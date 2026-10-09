struct Job { sitekey: String, pageurl: String, image_data: String }
fn setup(router: Router) { router.route("/in.php", handler); }
fn result() -> &'static str { "gRecaptchaResponse" }
