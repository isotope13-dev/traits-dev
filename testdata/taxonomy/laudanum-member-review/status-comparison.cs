class Handler {
    bool IsMissing(System.Web.HttpResponse Response) {
        return Response.StatusCode == 404;
    }
}
