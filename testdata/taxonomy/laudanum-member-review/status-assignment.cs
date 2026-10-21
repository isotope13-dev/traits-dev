class Handler {
    void Reject(System.Web.HttpResponse Response) {
        Response.StatusCode = 404;
    }
}
