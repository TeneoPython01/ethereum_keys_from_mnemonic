# the goal of this script is to generate Ethereum paper wallet keys        
# based on a mnemonic phrase (which is condusive to paper storage)         
# without using a website tool.  currently a common tool for key           
# and wallet derivation is https://iancoleman.io/bip39.  so, that          
# site can be used to test the output to ensure fidelity.  it is           
# recommended that you test this tool against the webiste using            
# a mnemonic that isn't for your wallet to prevent losing coins            
# to malware.                                                              

# how to use this script:                                                  
# 1) you will need to install the packages:                                
#      o pip install bip32                                                 
#      o pip install bip39                                                 
#      o pip install bip44                                                 
#    these libraries correspond to the BIPs (Bitcoin Improvement Proposals)
#    that can be found on the Bitcoin foudation's verified github:         
#    e.g., https://github.com/bitcoin/bips/blob/master/bip-0049.mediawiki  
# 2) set the variables at the beginning of the main() function, including  
#    the mnemonic phrase that you want to use                              
# 3) run the script                                                        

# if you want a mnemonic phrase to use as a test, the following one has    
# been used on other wallet / key scripts on github, so you can know it    
# won't expose you:                                                        
#                                                                          
# wise chief minute play violin then office horn wreck income wild cousin  
#                                                                          

from bip32 import BIP32, HARDENED_INDEX #used for overall root account keys
import bip39 # used to get seed from mnemonic phrase
import bip44 # used for wallet keys by derivation path
from bip44.utils import get_eth_addr # used to determine wallet address from path public key
import time


def pad_index_string(index, max_index):
    len_index = len(str(index))
    len_max_index = len(str(max_index))
    pad_size = len_max_index - len_index
    pad_str = ''
    for pad in range(0, pad_size):
        pad_str = pad_str + '0'
    index_str = pad_str + str(index)
    return index_str

def tab_level_str(level):
    tab_str = ''
    for i in range(0,level):
        tab_str = tab_str + '\t'
    return tab_str
        
def path_str_to_list(deriv_path_str):
    deriv_path_list = deriv_path_str.split('/')
    for i in range(0,5):
        if len(deriv_path_list) < 5:
            deriv_path_list.append('0')
    return deriv_path_list

def display_seed_data(mnemonic, tab_level):
    print(tab_level_str(tab_level) + '\n\n')
    print(tab_level_str(tab_level) + '==============================================')
    print(tab_level_str(tab_level) + 'GENERATING BIP32 and BIP 39 SEED AND KEY DATA:')
    print(tab_level_str(tab_level) + '==============================================\n')
    time.sleep(1) #pause the scrolling console output momentarily for readability

    print(tab_level_str(tab_level) + 'THE FOLLOWING TOP LEVEL INFORMATION IS THE SAME REGARDLESS OF TAB SELECTED ON https://iancoleman.io/bip39')
    print(tab_level_str(tab_level) + ' o BIP39 Mnemonic      : \t', mnemonic)
    print(tab_level_str(tab_level) + ' o BIP39 Seed          : \t', bip39.phrase_to_seed(mnemonic).hex())
    print(tab_level_str(tab_level) + ' o Coin                : \t', 'ETH - Ethereum') #hard coded
    print(tab_level_str(tab_level) + '')

    return 1

def display_acct_ext_keys_from_path(deriv_path, acct, tab_level):
    print(tab_level_str(tab_level) + ' o BIP32 Root Key      : \t', acct.get_master_xpriv())
    print(tab_level_str(tab_level) + '')
    print(tab_level_str(tab_level) + ' o Purpose             : \t', path_str_to_list(deriv_path)[1].replace("'",' (hardened)'))
    print(tab_level_str(tab_level) + ' o Coin                : \t', path_str_to_list(deriv_path)[2].replace("'",' (hardened)'))
    print(tab_level_str(tab_level) + ' o Account             : \t', path_str_to_list(deriv_path)[3].replace("'",'  (hardened)'))
    print(tab_level_str(tab_level) + ' o External / Internal : \t', path_str_to_list(deriv_path)[4].replace("'",'  (hardened)'))
    print(tab_level_str(tab_level) + '')
    print(tab_level_str(tab_level) + ' o Account Extended Private Key : \t', acct.get_xpriv_from_path(deriv_path))
    print(tab_level_str(tab_level) + ' o Account Extended Private Key : \t', acct.get_xpub_from_path(deriv_path))
    print(tab_level_str(tab_level) + '')


def display_bip32_ext_keys_from_path(deriv_path, acct, tab_level):
    print(tab_level_str(tab_level) + ' o Derivation Path            : \t', deriv_path)
    print(tab_level_str(tab_level) + ' o BIP32 Extended Private Key : \t', acct.get_xpriv_from_path(deriv_path))
    print(tab_level_str(tab_level) + ' o BIP32 Extended Public Key  : \t', acct.get_xpub_from_path(deriv_path))
    print(tab_level_str(tab_level) + '')


def display_wallets(number_of_wallets_to_generate, deriv_path_root, mnemonic, tab_level):
    print(tab_level_str(tab_level) + '=====================================================')
    print(tab_level_str(tab_level) + 'GENERATING {} WALLETS OF DATA SELECTED DERIVATION PATH'.format(str(number_of_wallets_to_generate)))
    print(tab_level_str(tab_level) + '=====================================================\n')

    for address_index in range(0, number_of_wallets_to_generate):
        deriv_path_plus_index = deriv_path_root + '/' + str(address_index)

        acct_with_index = bip44.Wallet(mnemonic = mnemonic)

        pk = acct_with_index.derive_public_key(path=deriv_path_plus_index)
        
        print(tab_level_str(tab_level) + '-> Derivation path {} : \t'.format(pad_index_string(address_index, number_of_wallets_to_generate)), deriv_path_plus_index)
        print(tab_level_str(tab_level) + '   Address         {} : \t'.format(pad_index_string(address_index, number_of_wallets_to_generate)), get_eth_addr(pk.hex()))
        print(tab_level_str(tab_level) + '   Public key      {} : \t'.format(pad_index_string(address_index, number_of_wallets_to_generate)), '0x'+acct_with_index.derive_public_key(path=deriv_path_plus_index).hex())
        print(tab_level_str(tab_level) + '   Private key     {} : \t'.format(pad_index_string(address_index, number_of_wallets_to_generate)), '0x'+acct_with_index.derive_secret_key(path=deriv_path_plus_index).hex())
        print(tab_level_str(tab_level) + '')

    return 1

def display_tab_banner(bip_str, tab_level):
    print(tab_level_str(tab_level) + '...............................................................................................')
    print(tab_level_str(tab_level) + '[{}] -- derivation path tab selected on https://iancoleman.io/bip39'.format(bip_str))
    if bip_str=='BIP32':
        print(tab_level_str(tab_level) + '           {}Note: dont forget to set custom derivation path in website if comparing values'.format(bip_str+' '))
    print(tab_level_str(tab_level) + '...............................................................................................')


def main():

    # SET THESE VARIABLES BEFORE RUNNING
    # ------------------------------------
    # 1) Create this many wallets in order starting with index 0
    number_of_wallets_to_generate = 3
    # 2) Your mnemonic phrase
    mnemonic='wise chief minute play violin then office horn wreck income wild cousin'
    # 3) Whether you want to show the BIP49, 84, and 141 tab section data which aren't working yet
    debug_bip_49  = 0 # 0 by default; 0 = hide section (not deriving properly yet); 1 = show the section
    debug_bip_84  = 0 # 0 by default; 0 = hide section (not deriving properly yet); 1 = show the section
    debug_bip_141 = 0 # 0 by default; 0 = hide section (not deriving properly yet); 1 = show the section

    #NOTE: standard Ethereum derivation path is "m/44'/60'/0'/0"; each wallet appends an index (like "m/44'/60'/0'/0/0")

    # CREATE THE ROOT ACCOUNT AND DETERMINE THE KEYS (BIP32)
    display_seed_data(
        mnemonic = mnemonic,
        tab_level = 0
        )

    # =========================================================================================
    #                             BIP32 TAB SECTION                                            
    # =========================================================================================

    #show the banner
    display_tab_banner(bip_str = 'BIP32', tab_level = 1)
    custom_deriv_path = "m/0"

    seed = bip39.phrase_to_seed(mnemonic) #convert mnemonic to seed (BIP39)
    acct_root = BIP32.from_seed(seed = seed) #create account object from seed

    #show the BIP32 extended key data
    display_bip32_ext_keys_from_path(
        deriv_path = custom_deriv_path,
        acct = acct_root,
        tab_level = 1
        )

    #show the wallets' data
    display_wallets(
        number_of_wallets_to_generate = number_of_wallets_to_generate,
        deriv_path_root = custom_deriv_path,
        mnemonic = mnemonic,
        tab_level = 2
        )

    # =========================================================================================
    #                             BIP44 TAB SECTION                                            
    # =========================================================================================

    #show the banner
    display_tab_banner(bip_str = 'BIP44', tab_level = 1)
    custom_deriv_path = "m/44'/60'/0'"

    #show the account extended key data
    display_acct_ext_keys_from_path(
        deriv_path = custom_deriv_path,
        acct = acct_root,
        tab_level = 1
        )

    #show the BIP32 extended key data
    display_bip32_ext_keys_from_path(
        deriv_path = custom_deriv_path,
        acct = acct_root,
        tab_level = 1
        )

    #show the wallets' data
    display_wallets(
        number_of_wallets_to_generate = number_of_wallets_to_generate,
        deriv_path_root = custom_deriv_path,
        mnemonic = mnemonic,
        tab_level = 2
        )

    # =========================================================================================
    #                             BIP49 TAB SECTION                                            
    # =========================================================================================

    #show the banner
    display_tab_banner(bip_str = 'BIP49', tab_level = 1)
    custom_deriv_path = "m/49'/60'/0'/0"

    #this code isn't working yet, so disabled by default
    if debug_bip_49 == 1:
        print('\t\t=====================================================')
        print('\t\tGENERATING {} WALLETS OF DATA SELECTED DERIVATION PATH'.format(str(number_of_wallets_to_generate)))
        print('\t\t=====================================================\n')

        for address_index in range(0, number_of_wallets_to_generate):
            deriv_path_plus_index = custom_deriv_path + '/' + str(address_index)

            acct_with_index = bip44.Wallet(mnemonic = mnemonic)

            pk = acct_with_index.derive_public_key(path=deriv_path_plus_index)
            
            print('\t\t-> Derivation path {} : \t'.format(pad_index_string(address_index, number_of_wallets_to_generate)), deriv_path_plus_index)
            print('\t\t   Address         {} : \t'.format(pad_index_string(address_index, number_of_wallets_to_generate)), '? Need to figure this out') #get_eth_addr(pk.hex())
            print('\t\t   Public key      {} : \t'.format(pad_index_string(address_index, number_of_wallets_to_generate)), '0x'+acct_with_index.derive_public_key(path=deriv_path_plus_index).hex())
            print('\t\t   Private key     {} : \t'.format(pad_index_string(address_index, number_of_wallets_to_generate)), '0x'+acct_with_index.derive_secret_key(path=deriv_path_plus_index).hex())
            print('')
    else:
        print('\t\t? Need to figure this out ?\n')

    # =========================================================================================
    #                             BIP84 TAB SECTION                                            
    # =========================================================================================

    display_tab_banner(bip_str = 'BIP84', tab_level = 1)
    #TODO - Show n Wallets using this custom derivation path as root
    custom_deriv_path = "m/84'/60'/0'/0"

    if debug_bip_84 == 1:
        print('\t\t=====================================================')
        print('\t\tGENERATING {} WALLETS OF DATA SELECTED DERIVATION PATH'.format(str(number_of_wallets_to_generate)))
        print('\t\t=====================================================\n')

        for address_index in range(0, number_of_wallets_to_generate):
            deriv_path_plus_index = custom_deriv_path + '/' + str(address_index)

            acct_with_index = bip44.Wallet(mnemonic = mnemonic)

            pk = acct_with_index.derive_public_key(path=deriv_path_plus_index)
            
            print('\t\t-> Derivation path {} : \t'.format(pad_index_string(address_index, number_of_wallets_to_generate)), deriv_path_plus_index)
            print('\t\t   Address         {} : \t'.format(pad_index_string(address_index, number_of_wallets_to_generate)), '? Need to figure this out') #get_eth_addr(pk.hex())
            print('\t\t   Public key      {} : \t'.format(pad_index_string(address_index, number_of_wallets_to_generate)), '0x'+acct_with_index.derive_public_key(path=deriv_path_plus_index).hex())
            print('\t\t   Private key     {} : \t'.format(pad_index_string(address_index, number_of_wallets_to_generate)), '0x'+acct_with_index.derive_secret_key(path=deriv_path_plus_index).hex())
            print('')
        print()    
    else:
        print('\t\t? Need to figure this one out ?\n')

    # =========================================================================================
    #                             BIP141 TAB SECTION                                            
    # =========================================================================================

    display_tab_banner(bip_str = 'BIP141', tab_level = 1)
    #TODO - Show n Wallets using this custom derivation path as root
    custom_deriv_path = "m/0"
    #TODO - Script semantics ?? like P2WPKH for example
    if debug_bip_141 == 1:
        print('\t\t=====================================================')
        print('\t\tGENERATING {} WALLETS OF DATA SELECTED DERIVATION PATH'.format(str(number_of_wallets_to_generate)))
        print('\t\t=====================================================\n')

        for address_index in range(0, number_of_wallets_to_generate):
            deriv_path_plus_index = custom_deriv_path + '/' + str(address_index)

            acct_with_index = bip44.Wallet(mnemonic = mnemonic)

            pk = acct_with_index.derive_public_key(path=deriv_path_plus_index)
            
            print('\t\t-> Derivation path {} : \t'.format(pad_index_string(address_index, number_of_wallets_to_generate)), deriv_path_plus_index)
            print('\t\t   Address         {} : \t'.format(pad_index_string(address_index, number_of_wallets_to_generate)), '? Need to figure this out') #get_eth_addr(pk.hex())
            print('\t\t   Public key      {} : \t'.format(pad_index_string(address_index, number_of_wallets_to_generate)), '0x'+acct_with_index.derive_public_key(path=deriv_path_plus_index).hex())
            print('\t\t   Private key     {} : \t'.format(pad_index_string(address_index, number_of_wallets_to_generate)), '0x'+acct_with_index.derive_secret_key(path=deriv_path_plus_index).hex())
            print('')
        print()
    else:
        print('\t\t? Need to figure this one out ?\n')

    #build wallet addresses branching off of the root account
    # and then display them.  they will always be in the same
    # order.

main()
