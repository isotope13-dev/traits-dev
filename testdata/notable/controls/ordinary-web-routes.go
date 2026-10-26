package application

func JwtAuthMiddleware() {}
func CookieAuthMiddleware() {}
func routes(router Router) {
    router.GET("/health", Health)
    router.Use(JwtAuthMiddleware())
    router.Use(CookieAuthMiddleware())
    logger.Info("CreatePayloadWebhook is an example name")
    logger.Info("CreateCredentialWebhook is another example name")
}
