// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title OrderEscrow
 * @dev Escrow contract for Farmer2Market platform
 * Holds payment in escrow until delivery is confirmed
 */
contract OrderEscrow {
    
    // Order states
    enum OrderState {
        CREATED,
        PAID,
        FARMER_CONFIRMED,
        OUT_FOR_DELIVERY,
        DELIVERED,
        FUNDS_RELEASED,
        REFUNDED,
        DISPUTED
    }
    
    // Order structure
    struct Order {
        uint256 orderId;
        address buyer;
        address farmer;
        uint256 amount;
        OrderState state;
        uint256 createdAt;
        uint256 completedAt;
        bytes32 proofHash;
    }
    
    // State variables
    address public admin;
    mapping(uint256 => Order) public orders;
    mapping(uint256 => bool) public orderExists;
    
    // Events
    event OrderCreated(uint256 indexed orderId, address buyer, address farmer, uint256 amount);
    event FarmerConfirmed(uint256 indexed orderId);
    event OutForDelivery(uint256 indexed orderId);
    event DeliveryProofSubmitted(uint256 indexed orderId, bytes32 proofHash);
    event FundsReleased(uint256 indexed orderId, address farmer, uint256 amount);
    event FundsRefunded(uint256 indexed orderId, address buyer, uint256 amount);
    event DisputeRaised(uint256 indexed orderId);
    
    // Modifiers
    modifier onlyAdmin() {
        require(msg.sender == admin, "Only admin can call this");
        _;
    }
    
    modifier orderMustExist(uint256 _orderId) {
        require(orderExists[_orderId], "Order does not exist");
        _;
    }
    
    constructor() {
        admin = msg.sender;
    }
    
    /**
     * @dev Create a new order in escrow
     * @param _orderId Unique order ID from backend
     * @param _buyer Buyer's wallet address
     * @param _farmer Farmer's wallet address
     */
    function createOrder(
        uint256 _orderId,
        address _buyer,
        address _farmer
    ) external payable onlyAdmin {
        require(!orderExists[_orderId], "Order already exists");
        require(_buyer != address(0), "Invalid buyer address");
        require(_farmer != address(0), "Invalid farmer address");
        require(msg.value > 0, "Amount must be greater than 0");
        
        orders[_orderId] = Order({
            orderId: _orderId,
            buyer: _buyer,
            farmer: _farmer,
            amount: msg.value,
            state: OrderState.PAID,
            createdAt: block.timestamp,
            completedAt: 0,
            proofHash: bytes32(0)
        });
        
        orderExists[_orderId] = true;
        
        emit OrderCreated(_orderId, _buyer, _farmer, msg.value);
    }
    
    /**
     * @dev Mark order as confirmed by farmer
     * @param _orderId Order ID
     */
    function markFarmerConfirmed(uint256 _orderId) 
        external 
        onlyAdmin 
        orderMustExist(_orderId) 
    {
        Order storage order = orders[_orderId];
        require(order.state == OrderState.PAID, "Order must be in PAID state");
        
        order.state = OrderState.FARMER_CONFIRMED;
        
        emit FarmerConfirmed(_orderId);
    }
    
    /**
     * @dev Mark order as out for delivery
     * @param _orderId Order ID
     */
    function markOutForDelivery(uint256 _orderId) 
        external 
        onlyAdmin 
        orderMustExist(_orderId) 
    {
        Order storage order = orders[_orderId];
        require(
            order.state == OrderState.FARMER_CONFIRMED, 
            "Order must be farmer confirmed"
        );
        
        order.state = OrderState.OUT_FOR_DELIVERY;
        
        emit OutForDelivery(_orderId);
    }
    
    /**
     * @dev Submit delivery proof and mark as delivered
     * @param _orderId Order ID
     * @param _proofHash Hash of delivery proof (image/document)
     */
    function submitDeliveryProof(uint256 _orderId, bytes32 _proofHash) 
        external 
        onlyAdmin 
        orderMustExist(_orderId) 
    {
        Order storage order = orders[_orderId];
        require(
            order.state == OrderState.OUT_FOR_DELIVERY, 
            "Order must be out for delivery"
        );
        require(_proofHash != bytes32(0), "Invalid proof hash");
        
        order.state = OrderState.DELIVERED;
        order.proofHash = _proofHash;
        
        emit DeliveryProofSubmitted(_orderId, _proofHash);
    }
    
    /**
     * @dev Release funds to farmer after successful delivery
     * @param _orderId Order ID
     */
    function releaseFunds(uint256 _orderId) 
        external 
        onlyAdmin 
        orderMustExist(_orderId) 
    {
        Order storage order = orders[_orderId];
        require(order.state == OrderState.DELIVERED, "Order must be delivered");
        require(order.amount > 0, "No funds to release");
        
        uint256 amount = order.amount;
        address farmer = order.farmer;
        
        order.state = OrderState.FUNDS_RELEASED;
        order.completedAt = block.timestamp;
        order.amount = 0; // Prevent re-entrancy
        
        // Transfer funds to farmer
        (bool success, ) = payable(farmer).call{value: amount}("");
        require(success, "Transfer to farmer failed");
        
        emit FundsReleased(_orderId, farmer, amount);
    }
    
    /**
     * @dev Refund buyer in case of dispute or cancellation
     * @param _orderId Order ID
     */
    function refundBuyer(uint256 _orderId) 
        external 
        onlyAdmin 
        orderMustExist(_orderId) 
    {
        Order storage order = orders[_orderId];
        require(
            order.state != OrderState.FUNDS_RELEASED && 
            order.state != OrderState.REFUNDED,
            "Cannot refund: funds already released or refunded"
        );
        require(order.amount > 0, "No funds to refund");
        
        uint256 amount = order.amount;
        address buyer = order.buyer;
        
        order.state = OrderState.REFUNDED;
        order.completedAt = block.timestamp;
        order.amount = 0; // Prevent re-entrancy
        
        // Transfer funds back to buyer
        (bool success, ) = payable(buyer).call{value: amount}("");
        require(success, "Transfer to buyer failed");
        
        emit FundsRefunded(_orderId, buyer, amount);
    }
    
    /**
     * @dev Raise a dispute for an order
     * @param _orderId Order ID
     */
    function raiseDispute(uint256 _orderId) 
        external 
        onlyAdmin 
        orderMustExist(_orderId) 
    {
        Order storage order = orders[_orderId];
        require(
            order.state != OrderState.FUNDS_RELEASED && 
            order.state != OrderState.REFUNDED,
            "Cannot dispute: order already completed"
        );
        
        order.state = OrderState.DISPUTED;
        
        emit DisputeRaised(_orderId);
    }
    
    /**
     * @dev Get order details
     * @param _orderId Order ID
     */
    function getOrder(uint256 _orderId) 
        external 
        view 
        orderMustExist(_orderId) 
        returns (
            address buyer,
            address farmer,
            uint256 amount,
            OrderState state,
            uint256 createdAt,
            uint256 completedAt,
            bytes32 proofHash
        ) 
    {
        Order memory order = orders[_orderId];
        return (
            order.buyer,
            order.farmer,
            order.amount,
            order.state,
            order.createdAt,
            order.completedAt,
            order.proofHash
        );
    }
    
    /**
     * @dev Transfer admin rights
     * @param _newAdmin New admin address
     */
    function transferAdmin(address _newAdmin) external onlyAdmin {
        require(_newAdmin != address(0), "Invalid address");
        admin = _newAdmin;
    }
    
    /**
     * @dev Get contract balance
     */
    function getBalance() external view returns (uint256) {
        return address(this).balance;
    }
}
