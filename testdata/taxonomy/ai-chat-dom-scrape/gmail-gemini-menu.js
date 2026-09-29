function addCloudHQMenuItem() {
  const menus = document.querySelectorAll("[role=menu]");
  menus.forEach((menu) => {
    const label = menu.getAttribute("aria-label") || "";
    if (label.indexOf("gemini") === -1 && label.indexOf("prompts") === -1) {
      return menu.querySelectorAll("[role=menuitem]");
    }
  });
}
