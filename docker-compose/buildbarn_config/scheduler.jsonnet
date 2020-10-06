local common = import 'common.libsonnet';

{
  global: { diagnosticsHttpListenAddress: ':7982' },
  adminHttpListenAddress: ':12345',
  clientGrpcServers: [{
    listenAddresses: [':8982'],
    authenticationPolicy: { allow: {} },
  }],
  workerGrpcServers: [{
    listenAddresses: [':8983'],
    authenticationPolicy: { allow: {} },
  }],
  browserUrl: common.browserUrl,
  contentAddressableStorage: common.blobstore.contentAddressableStorage,
  maximumMessageSizeBytes: common.maximumMessageSizeBytes,
}
