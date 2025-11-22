"""
Setup Verification Script
Run this to verify your environment is ready for the Quantamental pipeline
"""

import sys
from pathlib import Path

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print('='*60)

def check_python_version():
    """Check Python version"""
    print("\n🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor} (need 3.9+)")
        return False

def check_packages():
    """Check required packages"""
    print("\n📦 Checking required packages...")
    
    required = {
        'pandas': 'pandas',
        'numpy': 'numpy',
        'sklearn': 'scikit-learn',
        'wandb': 'wandb',
        'google.cloud.storage': 'google-cloud-storage',
        'yaml': 'pyyaml',
        'aiohttp': 'aiohttp',
        'matplotlib': 'matplotlib',
        'seaborn': 'seaborn',
    }
    
    all_good = True
    for module, package in required.items():
        try:
            __import__(module)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - Run: pip install {package}")
            all_good = False
    
    return all_good

def check_config_file():
    """Check if config.yaml exists"""
    print("\n⚙️  Checking configuration file...")
    
    config_path = Path("config.yaml")
    if config_path.exists():
        print(f"   ✅ config.yaml found")
        return True
    else:
        print(f"   ❌ config.yaml not found")
        return False

def check_environment_variables():
    """Check environment variables"""
    print("\n🔑 Checking environment variables...")
    
    import os
    
    vars_to_check = {
        'FMP_API_KEY': 'Optional (can use config.yaml)',
        'WANDB_API_KEY': 'Optional (can use wandb login)',
        'GOOGLE_APPLICATION_CREDENTIALS': 'Optional (can use default credentials)',
    }
    
    for var, description in vars_to_check.items():
        if os.getenv(var):
            print(f"   ✅ {var} is set")
        else:
            print(f"   ℹ️  {var} not set - {description}")
    
    return True

def check_wandb_login():
    """Check W&B login status"""
    print("\n🎨 Checking W&B authentication...")
    
    try:
        import wandb
        api = wandb.Api()
        print(f"   ✅ W&B authenticated as: {api.default_entity or 'default'}")
        return True
    except Exception as e:
        print(f"   ❌ W&B not authenticated - Run: wandb login")
        print(f"      Error: {e}")
        return False

def check_gcs_access():
    """Check GCS access"""
    print("\n☁️  Checking GCS access...")
    
    try:
        from google.cloud import storage
        client = storage.Client()
        print(f"   ✅ GCS client initialized")
        print(f"      Project: {client.project or 'default'}")
        return True
    except Exception as e:
        print(f"   ⚠️  GCS access check failed")
        print(f"      This is OK if you'll configure credentials later")
        print(f"      Error: {e}")
        return False

def check_file_structure():
    """Check if all required files exist"""
    print("\n📁 Checking file structure...")
    
    required_files = [
        'config.yaml',
        'utils.py',
        'data_collect.py',
        'data_process.py',
        'model_train.py',
        'model_predict.py',
        'backtest.py',
        'main.py',
        'requirements.txt',
        'README.md',
    ]
    
    all_good = True
    for file in required_files:
        if Path(file).exists():
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} missing")
            all_good = False
    
    return all_good

def test_config_loading():
    """Test loading configuration"""
    print("\n🔧 Testing configuration loading...")
    
    try:
        from utils import load_config
        config = load_config()
        print(f"   ✅ Config loaded successfully")
        print(f"      W&B Project: {config['wandb']['project']}")
        print(f"      GCS Bucket: {config['gcs']['bucket_name']}")
        print(f"      Features: {len(config['features']['technical']) + len(config['features']['fundamental'])}")
        return True
    except Exception as e:
        print(f"   ❌ Config loading failed: {e}")
        return False

def print_summary(results):
    """Print summary of checks"""
    print_header("VERIFICATION SUMMARY")
    
    total = len(results)
    passed = sum(results.values())
    
    print(f"\n   Checks Passed: {passed}/{total}")
    
    if passed == total:
        print("\n   🎉 ALL CHECKS PASSED! You're ready to go!")
        print("\n   Next steps:")
        print("   1. Review SETUP_GUIDE.md")
        print("   2. Run: python main.py --step all")
    else:
        print("\n   ⚠️  Some checks failed. Please fix the issues above.")
        print("\n   Failed checks:")
        for check, passed in results.items():
            if not passed:
                print(f"      - {check}")

def main():
    print_header("QUANTAMENTAL MODEL - SETUP VERIFICATION")
    
    results = {
        'Python Version': check_python_version(),
        'Required Packages': check_packages(),
        'Config File': check_config_file(),
        'Environment Variables': check_environment_variables(),
        'W&B Authentication': check_wandb_login(),
        'GCS Access': check_gcs_access(),
        'File Structure': check_file_structure(),
        'Config Loading': test_config_loading(),
    }
    
    print_summary(results)
    
    return all(results.values())

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
