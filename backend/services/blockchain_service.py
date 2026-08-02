import json
import os
from web3 import Web3


class BlockchainService:

    def __init__(self):

        self.w3 = None
        self.contract = None
        self.enabled = False

        self.system_wallet = None
        self.system_private_key = None


    # -------------------------------------------------
    # Initialize Blockchain
    # -------------------------------------------------

    def init_app(self, app):

        provider_uri = app.config.get(
            "WEB3_PROVIDER_URI"
        )

        print(
            "[INFO] Blockchain Provider:",
            provider_uri
        )


        if not provider_uri:
            print(
                "[WARN] WEB3_PROVIDER_URI missing"
            )
            return


        try:

            self.w3 = Web3(
                Web3.HTTPProvider(
                    provider_uri,
                    request_kwargs={
                        "timeout": 10
                    }
                )
            )


            if self.w3.is_connected():

                self.enabled = True

                print(
                    "[INFO] Connected Blockchain:",
                    provider_uri
                )


                print(
                    "[INFO] Chain ID:",
                    self.w3.eth.chain_id
                )


                self._load_contract(app)

                self._load_system_wallet(app)


            else:

                print(
                    "[WARN] Blockchain connection failed"
                )


        except Exception as e:

            print(
                "[ERROR] Blockchain connection:",
                e
            )



    # -------------------------------------------------
    # Load Smart Contract (FIXED ABI)
    # -------------------------------------------------

    def _load_contract(self, app):

        address = app.config.get(
            "SMART_CONTRACT_ADDRESS"
        )


        abi_path = app.config.get(
            "SMART_CONTRACT_ABI_PATH"
        )


        if not address:

            print(
                "[WARN] Contract address missing"
            )
            return


        if not abi_path:

            print(
                "[WARN] ABI path missing"
            )
            return



        if not os.path.exists(abi_path):

            print(
                "[WARN] ABI file not found:",
                abi_path
            )
            return



        try:

            with open(
                abi_path,
                "r"
            ) as file:

                contract_json = json.load(file)



            # ===============================
            # FIX:
            # Handle Hardhat artifact
            # ===============================

            if isinstance(contract_json, dict):

                abi = contract_json.get(
                    "abi"
                )

            else:

                abi = contract_json



            if not abi:

                raise Exception(
                    "ABI missing inside JSON"
                )



            checksum_address = (
                Web3.to_checksum_address(
                    address
                )
            )


            self.contract = (
                self.w3.eth.contract(
                    address=checksum_address,
                    abi=abi
                )
            )


            print(
                "[INFO] Smart Contract Loaded:",
                checksum_address
            )


        except Exception as e:

            print(
                "[ERROR] Contract loading failed:",
                e
            )



    # -------------------------------------------------
    # Load Wallet
    # -------------------------------------------------

    def _load_system_wallet(self, app):


        self.system_wallet = app.config.get(
            "SYSTEM_WALLET_ADDRESS"
        )


        self.system_private_key = app.config.get(
            "SYSTEM_WALLET_PRIVATE_KEY"
        )


        if self.system_private_key:

            self.system_private_key = (
                self.system_private_key.strip()
            )



        if self.system_wallet and self.system_private_key:


            self.system_wallet = (
                Web3.to_checksum_address(
                    self.system_wallet
                )
            )


            print(
                "[INFO] Wallet Loaded:",
                self.system_wallet
            )


        else:

            print(
                "[WARN] Wallet missing"
            )



    # -------------------------------------------------
    # Send Transaction
    # -------------------------------------------------

    def _send_transaction(self, tx):


        signed_tx = (
            self.w3.eth.account.sign_transaction(
                tx,
                self.system_private_key
            )
        )


        tx_hash = (
            self.w3.eth.send_raw_transaction(
                signed_tx.raw_transaction
            )
        )


        receipt = (
            self.w3.eth.wait_for_transaction_receipt(
                tx_hash
            )
        )


        return receipt.transactionHash.hex()



    # -------------------------------------------------
    # Create Order
    # -------------------------------------------------

    def create_order_on_chain(
            self,
            order_id,
            buyer_address,
            farmer_address,
            amount_in_wei
    ):


        if not self.contract:

            return (
                f"0xmocked_{order_id}"
            )



        try:

            nonce = (
                self.w3.eth.get_transaction_count(
                    self.system_wallet
                )
            )


            tx = (
                self.contract.functions
                .createOrder(
                    int(order_id),
                    buyer_address,
                    farmer_address
                )
                .build_transaction({

                    "chainId":
                        self.w3.eth.chain_id,

                    "gas":
                        300000,

                    "gasPrice":
                        self.w3.eth.gas_price,

                    "nonce":
                        nonce,

                    "value":
                        amount_in_wei

                })
            )


            result = self._send_transaction(tx)


            print(
                "[INFO] Order Created:",
                result
            )


            return result



        except Exception as e:

            print(
                "[ERROR] Create Order:",
                e
            )

            return None



    # -------------------------------------------------
    # Execute Contract Function
    # -------------------------------------------------

    def _execute_contract(
            self,
            function_name,
            order_id,
            mock_name
    ):


        if not self.contract:

            return (
                f"0xmocked_{mock_name}_{order_id}"
            )


        try:

            nonce = (
                self.w3.eth.get_transaction_count(
                    self.system_wallet
                )
            )


            function = getattr(
                self.contract.functions,
                function_name
            )


            tx = (
                function(
                    int(order_id)
                )
                .build_transaction({

                    "chainId":
                        self.w3.eth.chain_id,

                    "gas":
                        200000,

                    "gasPrice":
                        self.w3.eth.gas_price,

                    "nonce":
                        nonce

                })
            )


            return self._send_transaction(tx)



        except Exception as e:

            print(
                f"[ERROR] {function_name}:",
                e
            )

            return None



    # -------------------------------------------------
    # Contract Actions
    # -------------------------------------------------

    def mark_farmer_confirmed(self, order_id):

        return self._execute_contract(
            "markFarmerConfirmed",
            order_id,
            "confirm"
        )


    def mark_out_for_delivery(self, order_id):

        return self._execute_contract(
            "markOutForDelivery",
            order_id,
            "delivery"
        )


    def release_funds(self, order_id):

        return self._execute_contract(
            "releaseFunds",
            order_id,
            "release"
        )


    def refund_buyer(self, order_id):

        return self._execute_contract(
            "refundBuyer",
            order_id,
            "refund"
        )



    # -------------------------------------------------
    # Delivery Proof
    # -------------------------------------------------

    def submit_delivery_proof(
            self,
            order_id,
            proof_hash
    ):


        try:

            if isinstance(proof_hash, str):

                proof_hash = bytes.fromhex(
                    proof_hash.replace(
                        "0x",
                        ""
                    )
                )



            nonce = (
                self.w3.eth.get_transaction_count(
                    self.system_wallet
                )
            )


            tx = (
                self.contract.functions
                .submitDeliveryProof(
                    int(order_id),
                    proof_hash
                )
                .build_transaction({

                    "chainId":
                        self.w3.eth.chain_id,

                    "gas":
                        150000,

                    "gasPrice":
                        self.w3.eth.gas_price,

                    "nonce":
                        nonce

                })
            )


            return self._send_transaction(tx)



        except Exception as e:

            print(
                "[ERROR] Delivery Proof:",
                e
            )

            return None



    # -------------------------------------------------
    # Status
    # -------------------------------------------------

    def get_status(self):

        return {

            "connected":
                self.enabled,

            "chain_id":
                self.w3.eth.chain_id
                if self.w3
                else None,

            "contract_loaded":
                self.contract is not None

        }



    # -------------------------------------------------
    # Hash Generator
    # -------------------------------------------------

    def generate_hash(self, data):

        return Web3.keccak(
            text=data
        ).hex()



# Singleton

blockchain_service = BlockchainService()