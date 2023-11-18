import os
import csv
import time
import logging
from dotenv import load_dotenv
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solana.rpc.api import Client
from solders.system_program import TransferParams, transfer
from solana.transaction import Transaction

LAMPORTS_PER_SOL = 1_000_000_000

class SolanaWalletManager:
    def __init__(self, rpc_url, sender_private_key, delay_between_transactions, logger, csv_file_path='wallets.csv'):
        self.rpc_url = rpc_url
        self.sender_private_key = sender_private_key
        self.delay_between_transactions = delay_between_transactions
        self.logger = logger
        self.csv_file_path = csv_file_path

        # Set up Solana client
        self.sender = Keypair.from_base58_string(self.sender_private_key)
        self.solana_client = Client(self.rpc_url)

    def check_balance(self):
        return self.solana_client.get_balance(self.sender.pubkey())

    def load_wallets_from_csv(self):
        wallets = []
        with open(self.csv_file_path, 'r') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                address = row[0].strip()
                solana_amount = float(row[1].strip())
                lamports = int(solana_amount * LAMPORTS_PER_SOL)
                receiver = Pubkey.from_string(address)
                wallets.append((receiver, lamports))
        return wallets

    def total_solana_to_distribute(self):
        total = 0
        with open(self.csv_file_path, 'r') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                fees_and_sol = 0.000005 + float(row[1].strip())
                total += fees_and_sol
        return total

    def perform_transaction(self, receiver, lamports):
        transfer_ix = transfer(TransferParams(from_pubkey=self.sender.pubkey(), to_pubkey=receiver, lamports=lamports))
        txn = Transaction().add(transfer_ix)
        try:
            result = self.solana_client.send_transaction(txn, self.sender).value
            self.logger.info(f'SUCCESS - Sent {lamports / LAMPORTS_PER_SOL} SOL to {receiver} - Signature: {result}')
            return True
        except Exception as e:
            self.logger.error(f'Transaction failed for {receiver} - Error: {e}')
            return False

    def process_wallets(self):
        wallets = self.load_wallets_from_csv()
        wallets_failed = 0
        wallets_succeeded = 0

        for receiver, lamports in wallets:
            if self.perform_transaction(receiver, lamports):
                wallets_succeeded += 1
            else:
                wallets_failed += 1

            time.sleep(self.delay_between_transactions)

        self.logger.info(f"""
        -------------------------------------------------------------------------
        -------------------------------------------------------------------------
        Total Wallets Succeeded: {wallets_succeeded}
        Total Wallets Failed: {wallets_failed}

        Check logs.txt file for errors and other details.
        -------------------------------------------------------------------------
        -------------------------------------------------------------------------
        """)

# Load environment variables
load_dotenv()
rpc_url = os.getenv("SOLANA_RPC_URL")
sender_private_key = os.getenv("SENDER_WALLET_PRIVATE_KEY_BASE58")
delay_between_transactions = int(os.getenv("DELAY_IN_SECONDS_BETWEEN_TRANSACTIONS"))

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler('logs.txt')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger = logging.getLogger()
logger.addHandler(file_handler)

# Example usage:
wallet_manager = SolanaWalletManager(rpc_url=rpc_url, sender_private_key=sender_private_key, delay_between_transactions=delay_between_transactions, logger=logger)

# check if balance to be distributed is available in the sender wallet
wallet_balance_in_lamports = wallet_manager.check_balance().value
wallet_balance_in_sol = wallet_balance_in_lamports/LAMPORTS_PER_SOL
total_solana_to_distribute = wallet_manager.total_solana_to_distribute()
if total_solana_to_distribute > wallet_balance_in_sol:
    logger.error(f"Your distribution amount ({total_solana_to_distribute} SOL) is higher than the balance in your sender wallet ({wallet_balance_in_sol} SOL).")
else:
    logger.info("=========================================================================")
    logger.info("================================= START =================================")
    logger.info("=========================================================================")
    logger.info(f"Total Balance in Sender Wallet: {wallet_balance_in_sol} SOL")
    logger.info(f"Total Balance in wallets.csv to distribute: {total_solana_to_distribute} SOL")
    logger.info("=========================================================================")
    wallet_manager.process_wallets()