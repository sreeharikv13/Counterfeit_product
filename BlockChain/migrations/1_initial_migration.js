const Migrations = artifacts.require("StructDemo");

module.exports = function (deployer) {
    deployer.deploy(Migrations);
};
