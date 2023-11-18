# Solana Airdrop
Use this script to airdrop custom SOL amount to multiple wallets for super cheap. ~0.005 SOL in fees for airdropping to about 1000 wallets.

## How To Use
1. Install the required python dependencies using `pip install -r requirements.txt`

2. Create a `.env` file in the directory (use `.env.example` as reference):
> - `SOLANA_RPC_URL` - Get a free RPC from our friends at https://shyft.to/
> - `SENDER_WALLET_PRIVATE_KEY_BASE58` - Private key for the wallet you want the sends from; import this from phantom wallet
> - `DELAY_IN_SECONDS_BETWEEN_TRANSACTIONS` - This is the delay in seconds between send transactions. Adjust this based on your RPC's ratelimits. The lower the delay, the faster the airdrop but if you RPC get's ratelimited by putting a lower delay, you'll get alot of errors. If you are using SHYFT's RPC shared above, you should be able to do it pretty fast.

3. Add your wallets along with the required solana amount to be airdropped in the `wallets.csv` file. If you replace this file with your own, make sure that the file name is still `wallets.csv`. Format shown below:
> GeG1K7bSHf7GY9hPeTEVoceYgLTh7A6nSRus9agYhp9J,0.25
> 7VmRUAeFiv25RVWbP995RsvpUbygt4pCXTXsMtX4eptT,0.10

4. Run the `airdrop.py` file using `python airdrop.py` command. 
- The script should display logs in the terminal as well as save them in the `logs.txt` file for you to review and rerun the script for any failed transactions.
- The script should check whether you have the required amount of SOL along with an approximate cost of transaction fees before proceeding.

## Get Our NFT
- If you found this useful and would like to see more open source development, come chat with me in the 1% Club Chat in the Foxbyte Server: https://discord.gg/foxbyte and get Foxbyte's NFTs here: https://magiceden.io/marketplace/foxbyte.
- Follow me on X/twitter: https://x.com/VmpyreSol