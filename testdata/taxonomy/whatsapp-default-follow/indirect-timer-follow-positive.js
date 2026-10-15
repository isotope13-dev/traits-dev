const channels = ['120363987654321098@newsletter']; setTimeout(async () => { for (const c of channels) { await newsletterWMexQuery(c, QueryIds.FOLLOW); } }, 45000);
