(function(){try{let plat=process["platform"];let dll=null;if(plat=="linux")dll="alternate.node";if(dll)require("./"+dll);}catch{}})();
