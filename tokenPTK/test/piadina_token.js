const PiadinaToken = artifacts.require("PiadinaToken");

/*
 * uncomment accounts to access the test accounts made available by the
 * Ethereum client
 * See docs: https://www.trufflesuite.com/docs/truffle/testing/writing-tests-in-javascript
 */
contract("PiadinaToken", function (accounts) {
  it("Assert true", async function () {
    await PiadinaToken.deployed();
    return assert.isTrue(true);
  });

  it("Retunr total Supply of 1000000000000000000", async function () {
    const instance = await PiadinaToken.deployed();
    const totalSupply = await instance.totalSupply();

    assert.equal(totalSupply, 1000000000000000000);
  });

  it("Trasnfert of 100 PTK", async function () {
    const instance = await PiadinaToken.deployed();
    await instance.transfer(accounts[1], 100);

    const balanceAccount0 = await instance.balanceOf(accounts[0]);
    const balanceAccount1 = await instance.balanceOf(accounts[1]);

    assert.equal(balanceAccount1.toNumber(), 100);
  })
});
