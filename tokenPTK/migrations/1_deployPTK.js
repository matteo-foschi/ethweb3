const PiadinaToken = artifacts.require("PiadinaToken");

module.exports = (deployer) => {
  deployer.deploy(PiadinaToken, "PiadinaToken", "PKT", 1);
};