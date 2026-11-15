---
name: feishu-create
description: Create a Feishu document
---

创建文档后必须立即给 `user@example.com` 授予 `full_access` 权限。
`feishu-cli perm add <document_id> --member-type email --member-id user@example.com --perm full_access`
