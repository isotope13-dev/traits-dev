package operator
import webcontroller "github.com/its-a-feature/Mythic/webserver/controllers"
import "github.com/its-a-feature/Mythic/authentication"
func routes(router Router) {
    router.POST("/agent_message", webcontroller.AgentMessageWebhook)
    router.POST("/create_task", webcontroller.CreateTaskWebhook)
    router.POST("/create_payload", webcontroller.CreatePayloadWebhook)
    router.Use(authentication.JwtAuthMiddleware())
    router.Use(authentication.CookieAuthMiddleware())
}
