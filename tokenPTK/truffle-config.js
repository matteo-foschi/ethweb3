module.exports = {
  networks: {
    development: {
      host: "0.0.0.0", // Localhost (default: none)
      port: 8545, // Standard Ethereum port (default: none)
      network_id: "1337", // Any network (default: none)
    },
  },
  compilers: {
    solc: {
      version: "0.8.0",
    },
  },
}