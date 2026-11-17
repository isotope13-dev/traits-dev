const service = NodeIKernelLoginService.get()
service.addKernelLoginListener({
  onQRCodeGetPicture(data) {
    sendToPipe({ kind: 'qrcode', pngBase64QrcodeData: data.pngBase64QrcodeData })
  }
})
