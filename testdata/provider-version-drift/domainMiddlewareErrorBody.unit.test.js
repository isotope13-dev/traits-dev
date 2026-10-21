import { i18nMiddleware } from "@prosopo/locale";
import { getLogger } from "@prosopo/logger";
import express from "express";
import { afterAll, beforeAll, describe, expect, it, vi } from "vitest";
import { domainMiddleware } from "../../../api/domainMiddleware.js";
const { getClientRecord } = vi.hoisted(() => ({
    getClientRecord: vi.fn(),
}));
vi.mock("../../../tasks/index.js", () => ({
    Tasks: class {
        constructor() {
            this.db = { getClientRecord };
            this.clientTaskManager = {
                domainPatternMatcher: (_referrer, _domain) => false,
            };
        }
    },
}));
const SITE_KEY = "5GrwvaEF5zXb26Fz9rcQpDWS57CtERHpNehXCPcNoHGKutQY";
const SECRET = "mongodb://admin:hunter2@10.0.0.5:27017/provider";
describe("domainMiddleware error bodies", () => {
    let server;
    let baseUrl;
    beforeAll(async () => {
        const app = express();
        app.use(express.json());
        app.use((req, _res, next) => {
            req.logger = getLogger("error", "test:domain-middleware-error");
            next();
        });
        app.use(await i18nMiddleware({}));
        const env = {};
        app.use(domainMiddleware(env));
        app.post("/client", (_req, res) => {
            res.json({ reached: true });
        });
        server = app.listen(0, "127.0.0.1");
        await new Promise((resolve) => server.once("listening", resolve));
        const address = server.address();
        if (address === null || typeof address === "string")
            throw new Error("test server has no TCP address");
        baseUrl = `http://127.0.0.1:${address.port}`;
    });
    afterAll(async () => {
        await new Promise((resolve) => server.close(() => resolve()));
    });
    it("does not return a thrown non-API error to the caller", async () => {
        getClientRecord.mockRejectedValueOnce(Object.assign(new Error("connect failed"), { errmsg: SECRET }));
        const res = await fetch(`${baseUrl}/client`, {
            method: "POST",
            headers: {
                "content-type": "application/json",
                origin: "https://site.example",
                "prosopo-site-key": SITE_KEY,
            },
            body: JSON.stringify({ dapp: SITE_KEY }),
        });
        const text = await res.text();
        expect(res.status).toBe(401);
        expect(text).not.toContain("hunter2");
        expect(JSON.parse(text)).toEqual({
            error: "Unauthorized",
            message: "Unauthorized",
        });
    });
});
//# sourceMappingURL=domainMiddlewareErrorBody.unit.test.js.map