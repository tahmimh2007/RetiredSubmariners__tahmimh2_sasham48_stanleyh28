// ─────────────────────────────────────────────────────────────
//  Unified chart rendering & download handlers
// ─────────────────────────────────────────────────────────────
let activeChart = null;

document.addEventListener('DOMContentLoaded', () => {
  if (!window.graph) return;
  switch (graph) {
    case 'bar':     activeChart = renderBar();     break;
    case 'line':    activeChart = renderLine();    break;
    case 'scatter': activeChart = renderScatter(); break;
  }
});

function renderBar() {
  const series = labels.map((lbl,i)=>( { name: lbl, data: y_lists[i] } ));
  const options = {
    chart: { type:'bar', height:400, width: Math.max(800,x.length*40) },
    series,
    xaxis: { categories:x, title:{text:'Independent Variable'} },
    yaxis: { title:{text:'Dependent Variables'} },
    plotOptions: { bar:{horizontal:false,columnWidth:'20px'}},
    dataLabels:{enabled:true},
    title:{text:'Bar Graph'}
  };
  const c = new ApexCharts(document.querySelector('#chart'), options);
  c.render();
  return c;
}

function renderLine() {
  const isNum = x.every(v=>!isNaN(v));
  const idx = isNum
    ? x.map((v,i)=>( {v,i} )).sort((a,b)=>a.v-b.v).map(o=>o.i)
    : null;
  const series = isNum
    ? y_lists.map((ys,s)=>( { name: labels[s], data: idx.map(i=>( {x:x[i],y:ys[i]} )) } ))
    : y_lists.map((ys,i)=>( { name: labels[i], data: ys } ));
  const opts = {
    chart:{type:'line',height:350},
    series, xaxis:{type:isNum?'numeric':'category'},
    yaxis:{title:{text:'Dependent Variables'}},
    stroke:{curve:'smooth',width:2},markers:{size:4},
    tooltip:{shared:true,intersect:false},
    title:{text:'Line Graph'}
  };
  const c = new ApexCharts(document.querySelector('#chart'), opts);
  c.render();
  return c;
}

function renderScatter() {
  const isNum = x.every(v=>!isNaN(v));
  const idx = isNum
    ? x.map((v,i)=>( {v,i} )).sort((a,b)=>a.v-b.v).map(o=>o.i)
    : null;
  const series = isNum
    ? y_lists.map((ys,s)=>( { name: labels[s], data: idx.map(i=>( {x:x[i],y:ys[i]} )) } ))
    : y_lists.map((ys,i)=>( { name: labels[i], data: ys } ));
  const opts = {
    chart:{type:'scatter',height:350,zoom:{enabled:true,type:'xy'}},
    series, xaxis:{type:isNum?'numeric':'category',title:{text:'Independent Variable'}},
    yaxis:{title:{text:'Dependent Variables'}},
    markers:{size:6},tooltip:{shared:false,intersect:true},
    title:{text:'Scatter Plot'}
  };
  const c = new ApexCharts(document.querySelector('#chart'), opts);
  c.render();
  return c;
}

// download handlers
window.downloadChart = fmt=>{
  if(!activeChart) return;
  activeChart.dataURI().then(({imgURI,svgURI})=>{
    const uri = fmt==='svg'?svgURI:imgURI;
    const link = document.createElement('a');
    link.download = `chart.${fmt}`; link.href = uri; link.click();
  });
};

window.downloadCSV = ()=>{
  if(!activeChart) return;
  const hdrs = labels;
  const rows = x.map((xv,i)=>( [xv, ...y_lists.map(ys=>ys[i])] ));
  let csv = hdrs.join(',') + '\n' + rows.map(r=>r.join(',')).join('\n');
  const blob = new Blob([csv],{type:'text/csv;charset=utf-8;'});
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'chart.csv'; document.body.append(a); a.click(); a.remove();
};