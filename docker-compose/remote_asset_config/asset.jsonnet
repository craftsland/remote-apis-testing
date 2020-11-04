{
  fetcher: {
    caching: {
      fetcher: {
        http: {
          allowUpdatesForInstances: ['remote-execution'],
          contentAddressableStorage: {
            grpc: {
              address: "frontend:8980"
  }}}}}},


  assetStore: {
    circular: {
      directory: '/storage',
      offsetFileSizeBytes: 1024 * 1024,
      offsetCacheSize: 1000,
      dataFileSizeBytes: 100 * 1024 * 1024,
      dataAllocationChunkSizeBytes: 1048576,
      instances: ['remote-execution'],
    },
  },
  httpListenAddress: ':7982',
  grpcServers: [{
    listenAddresses: [':8979'],
    authenticationPolicy: { allow: {} },
  }],
  allowUpdatesForInstances: ['remote-execution'],
  maximumMessageSizeBytes: 16 * 1024 * 1024 * 1024,
}
