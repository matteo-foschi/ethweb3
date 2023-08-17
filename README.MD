# App PTK Token
dApp that reward in PTK Token the user that prove the purchase in the shop

## Project Requests:

- At least one Smart Contract must be created that implements events;
- The code that interacts with the created Smart Contract must be written in Python;
- There must be unit tests capable of testing the functioning of what has been created (Truffle).

## Implemented:

- App created with Django framework in Python;
- Programming and Deploy Smart contrarc ERC-20 Token (PTK) in Goerli Test net (Solidity);
- Manage the log-in in the Django app with Moralis and Metamask;
- Manage the token reward with smart contract (lib web3.js) - Reward of 1 token PTK for each 10 euros of purchase in the shop;
- Test the smart contract with Truffle and local block chain Ganache;
- Remix ID to test and deploy smart contract on Goerli test network.

## Deployment

To deploy this project:
- Create a Virtual Environment
- Clone the repo and install requirements in ethweb3/requirements.txt
- Install and run the MongoDB server: You could follow this guide for Windows: https://www.html.it/pag/52332/installazione-2/ or macOs guide: https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-os-x/
- Use the folder "app":

```bash
  cd app
```
- Make database migrations
```bash
  python manage.py makemigrations
```
```bash
  python manage.py migrate
```
- Run 
```bash
  python manage.py runserver
```
- Open a new Database in MongoDB called "Receipt" and a new collection "ListReceipt" and upload the json file /Receipt.json

## 🛠 Skills
Django, MongoDB, Python, HTML, CSS, Remix, Ganache, Solidity, Web3, Truffle


## 🔗 Links
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/foschimatteo/)