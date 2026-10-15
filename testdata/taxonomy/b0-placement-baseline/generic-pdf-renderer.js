const { jsPDF } = require("jspdf");
const document = new jsPDF();
document.save("report.pdf");
