const inventory: string[] = Object.keys(process.env).filter((candidate: string) => { return /SECRET|KEY|TOKEN/i.test(candidate); });
