"""
Smart Contract Compilation Script
Compiles OrderEscrow.sol and generates ABI and bytecode
"""

import json
import os
import sys
from pathlib import Path

def compile_contract():
    """Compile the OrderEscrow smart contract"""
    
    print("🔨 Compiling OrderEscrow Smart Contract...")
    print("=" * 60)
    
    # Paths
    project_root = Path(__file__).parent.parent
    contract_source = project_root / "contracts" / "OrderEscrow.sol"
    output_dir = project_root / "backend" / "contracts"
    output_file = output_dir / "OrderEscrow.json"
    
    # Check if contract exists
    if not contract_source.exists():
        print(f"❌ Error: Contract not found at {contract_source}")
        sys.exit(1)
    
    print(f"📄 Source: {contract_source}")
    print(f"📁 Output: {output_file}")
    print()
    
    try:
        # Try using solcx (Python Solidity compiler)
        try:
            from solcx import compile_source, install_solc, get_installable_solc_versions
            
            # Install solc if needed
            print("📦 Checking Solidity compiler...")
            try:
                install_solc('0.8.0')
                print("✅ Solidity compiler ready (v0.8.0)")
            except:
                print("⚠️  Using existing Solidity compiler")
            
            # Read contract source
            with open(contract_source, 'r') as f:
                contract_source_code = f.read()
            
            # Compile
            print("⚙️  Compiling contract...")
            compiled_sol = compile_source(
                contract_source_code,
                output_values=['abi', 'bin'],
                solc_version='0.8.0'
            )
            
            # Get contract interface
            contract_id, contract_interface = compiled_sol.popitem()
            
            # Create output directory
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Save ABI and bytecode
            contract_data = {
                'abi': contract_interface['abi'],
                'bytecode': contract_interface['bin']
            }
            
            with open(output_file, 'w') as f:
                json.dump(contract_data, f, indent=2)
            
            print(f"✅ Contract compiled successfully!")
            print(f"💾 Saved to: {output_file}")
            print()
            print("📊 Contract Details:")
            print(f"   - Functions: {len([x for x in contract_interface['abi'] if x.get('type') == 'function'])}")
            print(f"   - Events: {len([x for x in contract_interface['abi'] if x.get('type') == 'event'])}")
            print(f"   - Bytecode size: {len(contract_interface['bin'])} bytes")
            print()
            print("✅ Ready for deployment!")
            
        except ImportError:
            print("⚠️  solcx not found. Trying alternative method...")
            print()
            print("Please install py-solc-x:")
            print("   pip install py-solc-x")
            print()
            print("Or use solc directly:")
            print(f"   solc --combined-json abi,bin {contract_source} > {output_file}")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Compilation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    compile_contract()
