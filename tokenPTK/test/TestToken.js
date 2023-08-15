const PiadinaToken = artifacts.require('PiadinaToken');  // Replace with your token contract's name

describe('PiadinaToken', function () {
  it('should have the correct symbol', async function () {
    const tokenInstance = await PiadinaToken.deployed();
    const tokenSymbol = await tokencInstance.symbol();

    expect(tokenSymbol).to.equal('PTK');  // Replace with the expected symbol
  });
