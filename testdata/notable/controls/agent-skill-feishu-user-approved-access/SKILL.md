---
name: feishu-create
description: Create a Feishu document
---

不要自动授予任何权限。只有用户明确授权后，才根据用户提供的收件人配置访问权限。
`feishu-cli perm add <document_id> --member-type email --member-id <recipient> --perm full_access`
