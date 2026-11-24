package integration

func verifyRole() {
 checkIAMApiErr()
}
var trust = `{"Effect":"Allow","Principal":{"AWS":"*"},"Action":"sts:AssumeRole"}`
