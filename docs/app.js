// 康波周期投资预测平台 - 核心逻辑
// === DATA ===
const scores={
  '黄金':{z:5,s:5,t:5,b:5,msg:'四维满分共振！康波萧条期最佳资产+去美元化趋势+货币重置核心锚+法币贬值终极对冲。黄金是唯一四个维度都满分的标的——它不是投资品，它是货币本身。'},
  '白银':{z:4,s:5,t:4,b:4,msg:'新能源工业属性加持，金银比修复空间大。大贬值背景下，白银是"穷人的黄金"，弹性甚至更大。'},
  'AI算力':{z:5,s:5,t:3,b:2,msg:'第六轮康波核心基建，算力是AI的电力。但算力是法币计价的服务，在大贬值维度评分偏低——需要持续投入法币购买。'},
  '核电':{z:4,s:5,t:3,b:2,msg:'AI用电量暴增+碳中和双驱动。核电是实体基建，有一定硬资产属性，但主要受电力政策驱动。'},
  '小金属':{z:4,s:5,t:5,b:4,msg:'镓锗锑稀土是AI+新能源的"维生素"，供给高度集中。实物小金属在大贬值背景下具备硬资产属性。四维共振仅次于黄金。'},
  '美股':{z:4,s:4,t:2,b:1,msg:'AI革命主战场，但法币计价的金融资产在大贬值维度只评1分——看似上涨，实际购买力在下降。'},
  '美债':{z:3,s:3,t:2,b:1,msg:'利率下行周期有短期机会。但美元长期信用风险+债务不可持续，大贬值维度只评1分——法币债务的终极受害者。'},
  '中药材':{z:3,s:4,t:3,b:3,msg:'老龄化+中国特色消费+稀缺性。中药材具有实物属性，大贬值背景下有一定保值功能。'},
  '加密货币':{z:3,s:3,t:4,b:3,msg:'去中心化货币实验，是货币重置的技术路径之一。但波动性太大，大贬值维度给3分——方向对，确定性不足。'},
  '房地产':{z:2,s:2,t:2,b:3,msg:'康波下行+调整期+泡沫风险。但房产是实物资产，大贬值背景下有一定保值功能——核心地段>非核心。'},
  'A股':{z:3,s:3,t:3,b:2,msg:'国产替代+AI概念有机会，但法币计价的金融资产在大贬值中承压。结构性机会大于整体。'},
  '大宗商品':{z:4,s:4,t:4,b:5,msg:'资源超级牛市逻辑成立。在大贬值维度满分——实物商品是法币贬值的直接对冲工具。四维共振仅次于黄金。'},
  '现金':{z:2,s:2,t:3,b:1,msg:'萧条末期持有过多现金将错失底部机会。大贬值维度只评1分——现金是大贬值的最大输家。'},
  '人民币资产':{z:3,s:3,t:3,b:3,msg:'人民币国际化趋势确定，大贬值背景下人民币相对美元可能反而走强——全球货币重置的受益者。'},
  '东南亚市场':{z:4,s:4,t:3,b:3,msg:'产业转移+人口红利+去中国化受益者。东南亚国家持有大量美元外储，大贬值中面临挑战但也蕴含机会。'}
};
const assets={
  depression_late:{best:['核心资产（底部买入）','黄金','白银'],good:['股票（逢低布局）','大宗商品','AI算力'],avoid:['过度持有现金','高杠杆资产','长期债券']},
  recovery:{best:['股票（成长股）','AI算力','大宗商品'],good:['核心城市房产','小金属','核电'],avoid:['现金（通胀侵蚀）','长期债券']},
  prosperity:{best:['房地产','实物资产'],good:['股票','消费类'],avoid:['债券','现金']},
  recession:{best:['黄金','大宗商品'],good:['现金'],avoid:['股票','房地产']},
  depression_early:{best:['现金','国债'],good:['黄金'],avoid:['股票','房地产','大宗商品']}
};
const assetsLabel={best:['🟢 最佳资产','label-green'],good:['🟡 可配置','label-yellow'],avoid:['🔴 应避免','label-red']};
const families=[
  {name:'洛克菲勒家族',country:'🇺🇸 美国',gen:'7代 · 150+年',wealth:'110-320亿美元',
   mech:['不可撤销王朝信托（Dynasty Trust）','瀑布方法——终身寿险+信托循环','家族办公室统筹全球投资','慈善基金会（声誉+税务+使命感）'],
   strategy:'萧条期加大股权和地产配置（逆向操作），繁荣期减持高估值资产。1929大萧条信托隔离保全核心资产。'},
  {name:'罗斯柴尔德家族',country:'🇪🇺 欧洲',gen:'6代 · 300年',wealth:'5万亿美元（含私人）',
   mech:['家族银行不上市，股权内部传承','联合融资（Syndicate）模式','锚定实体经济（矿产、土地、基础设施）','为交战双方融资，对冲地缘风险'],
   strategy:'繁荣期发行金融产品放大收益，萧条期收购低价实物资产。穿越拿破仑战争、两次世界大战。'},
  {name:'李嘉诚家族',country:'🇭🇰 中国香港',gen:'2代 · 万亿港元',wealth:'373-451亿美元',
   mech:['双轨制分家（实业+金融）','全球化分散（50+国家）','匮乏期骆驼式积累，充裕期狮子式警惕','家族办公室顶层设计风险对冲'],
   strategy:'萧条期大量收购基础设施，繁荣期减持高位资产。2013-2015大规模撤出中国房地产（精准逃顶）。'},
  {name:'沃尔顿家族',country:'🇺🇸 美国',gen:'3代',wealth:'5134亿美元（全球最富）',
   mech:['沃尔玛股权集中在家族信托','家族成员不直接参与管理','零售业务稳定现金流驱动多元化'],
   strategy:'稳定现金流穿越周期，利用萧条期进行科技和地产投资。'},
  {name:'华为/任正非',country:'🇨🇳 中国',gen:'1代 · 去家族化',wealth:'任正非个人210亿',
   mech:['98.6%股权分给员工（虚拟受限股）','去家族化，职业经理人治理','R&D投入15%+营收（逆周期加码）','全球化收入来源（170+国家）'],
   strategy:'技术驱动穿越周期，"华为的冬天"论——繁荣期提前准备萧条。员工持股制度确保逆周期不流失人才。'}
];
const waves=[
  {name:'第一轮 · 蒸汽机时代',period:'1780-1845',driver:'蒸汽机、纺织机械、铁路',phases:[{l:'🌱回升',y:'1780-1795',c:'spring'},{l:'☀️繁荣',y:'1795-1815',c:'summer'},{l:'🍂衰退',y:'1815-1830',c:'autumn'},{l:'❄️萧条',y:'1830-1845',c:'winter'}]},
  {name:'第二轮 · 钢铁铁路时代',period:'1845-1900',driver:'钢铁、铁路网、电报',phases:[{l:'🌱回升',y:'1845-1857',c:'spring'},{l:'☀️繁荣',y:'1857-1873',c:'summer'},{l:'🍂衰退',y:'1873-1885',c:'autumn'},{l:'❄️萧条',y:'1885-1900',c:'winter'}]},
  {name:'第三轮 · 电气化时代',period:'1900-1950',driver:'电气化、化工、汽车',phases:[{l:'🌱回升',y:'1900-1910',c:'spring'},{l:'☀️繁荣',y:'1910-1929',c:'summer'},{l:'🍂衰退',y:'1929-1937',c:'autumn'},{l:'❄️萧条',y:'1937-1950',c:'winter'}]},
  {name:'第四轮 · 石油化工时代',period:'1950-1990',driver:'石油化工、喷气机、电子',phases:[{l:'🌱回升',y:'1950-1958',c:'spring'},{l:'☀️繁荣',y:'1958-1973',c:'summer'},{l:'🍂衰退',y:'1973-1982',c:'autumn'},{l:'❄️萧条',y:'1982-1990',c:'winter'}]},
  {name:'第五轮 · 信息技术时代',period:'1990-2030',driver:'信息技术、互联网、移动通信',phases:[{l:'🌱回升',y:'1990-2000',c:'spring'},{l:'☀️繁荣',y:'2000-2008',c:'summer'},{l:'🍂衰退',y:'2008-2019',c:'autumn'},{l:'❄️萧条',y:'2019-2030',c:'winter',current:true}]},
  {name:'第六轮 · AI+生物科技+新能源',period:'2025-2070',driver:'人工智能、生物科技、新能源、量子计算',phases:[{l:'🌱回升',y:'2025-2038',c:'spring',current:true},{l:'☀️繁荣',y:'2038-2055',c:'summer'},{l:'🍂衰退',y:'2055-2065',c:'autumn'},{l:'❄️萧条',y:'2065-2070',c:'winter'}]}
];
// === INIT ===
document.addEventListener('DOMContentLoaded',()=>{initWaves();initFamilies();updateAssets();updateScore();updateAge()});
// === TAB ===
function showTab(i){
  document.querySelectorAll('.tab').forEach((t,j)=>t.classList.toggle('active',j===i));
  document.querySelectorAll('.panel').forEach((p,j)=>p.classList.toggle('active',j===i));
}
// === WAVES ===
function initWaves(){
  const el=document.getElementById('waveList');
  el.innerHTML=waves.map((w,i)=>{
    const isCurrent=i>=4;
    return `<div class="card wave-card" style="border-color:${isCurrent?'var(--green)':'var(--border)'}">
      <div class="wave-header" onclick="this.nextElementSibling.classList.toggle('open')">
        <div><h3>${w.name}</h3><div style="font-size:0.78em;color:var(--text2);margin-top:4px">${w.period} · ${w.driver}</div></div>
        ${isCurrent?'<span class="wave-badge badge-winter">当前</span>':'<span style="color:var(--text2);font-size:0.8em">▼</span>'}
      </div>
      <div class="wave-body${isCurrent?' open':''}">
        <div class="wave-detail">
          <div class="timeline">${w.phases.map(p=>`<div class="phase ${p.c}${p.current?' current':''}" style="flex:1">${p.l}<br><span style="font-size:0.8em">${p.y}</span></div>`).join('')}</div>
        </div>
      </div>
    </div>`;
  }).join('');
}
// === ASSETS ===
function updateAssets(){
  const phase=document.getElementById('phaseSelect').value;
  const d=assets[phase];
  const el=document.getElementById('assetResult');
  el.innerHTML=['best','good','avoid'].map(k=>{
    const[label,cls]=assetsLabel[k];
    return `<div style="margin-top:14px"><div class="${cls}" style="font-weight:600;margin-bottom:6px">${label}</div>
      <div class="asset-grid">${d[k].map(a=>`<div class="asset-item asset-${k==='best'?'best':k==='good'?'good':'avoid'}">${a}</div>`).join('')}</div></div>`;
  }).join('');
}
// === RADAR (4D) ===
function drawRadar(z,s,t,b){
  const c=document.getElementById('radar');
  const ctx=c.getContext('2d');
  const cx=155,cy=155,r=110;
  ctx.clearRect(0,0,310,310);
  const angles=[-Math.PI/2, 0, Math.PI/2, Math.PI];
  const labels=['周金涛\n(周期定位)','时寒冰\n(趋势方向)','巴拉塔\n(货币重置)','宋鸿兵\n(货币环境)'];
  const vals=[z/5,s/5,b/5,t/5];
  // Grid
  for(let lv=1;lv<=5;lv++){
    ctx.beginPath();
    const lr=r*lv/5;
    angles.forEach((a,i)=>{
      const x=cx+lr*Math.cos(a),y=cy+lr*Math.sin(a);
      i===0?ctx.moveTo(x,y):ctx.lineTo(x,y);
    });
    ctx.closePath();
    ctx.strokeStyle='rgba(255,255,255,0.08)';
    ctx.stroke();
  }
  // Axes
  angles.forEach(a=>{
    ctx.beginPath();
    ctx.moveTo(cx,cy);
    ctx.lineTo(cx+r*Math.cos(a),cy+r*Math.sin(a));
    ctx.strokeStyle='rgba(255,255,255,0.15)';
    ctx.stroke();
  });
  // Data polygon
  ctx.beginPath();
  const pts=angles.map((a,i)=>({x:cx+r*vals[i]*Math.cos(a),y:cy+r*vals[i]*Math.sin(a)}));
  pts.forEach((p,i)=>{i===0?ctx.moveTo(p.x,p.y):ctx.lineTo(p.x,p.y)});
  ctx.closePath();
  ctx.fillStyle='rgba(0,212,170,0.25)';
  ctx.fill();
  ctx.strokeStyle='#00d4aa';
  ctx.lineWidth=2;
  ctx.stroke();
  // Dots
  pts.forEach(p=>{ctx.beginPath();ctx.arc(p.x,p.y,5,0,Math.PI*2);ctx.fillStyle='#00d4aa';ctx.fill()});
  // Labels
  const lOff=[{x:0,y:-20},{x:18,y:5},{x:0,y:20},{x:-18,y:5}];
  angles.forEach((a,i)=>{
    const lx=cx+(r+28)*Math.cos(a)+lOff[i].x;
    const ly=cy+(r+28)*Math.sin(a)+lOff[i].y;
    ctx.fillStyle='#94a3b8';
    ctx.font='11px sans-serif';
    ctx.textAlign='center';
    labels[i].split('\n').forEach((line,li)=>{
      ctx.fillText(line,lx,ly+li*13);
    });
  });
  // Value labels
  angles.forEach((a,i)=>{
    const px=cx+r*vals[i]*Math.cos(a),py=cy+r*vals[i]*Math.sin(a);
    ctx.fillStyle='#fff';
    ctx.font='bold 13px sans-serif';
    ctx.textAlign='center';
    const off=vals[i]>0.6?-12:12;
    ctx.fillText([z,s,b,t][i]+'/5',px,py+off);
  });
}
function updateScore(){
  const name=document.getElementById('investSelect').value;
  const d=scores[name];
  const avg=((d.z+d.s+d.t+d.b)/4).toFixed(1);
  drawRadar(d.z,d.s,d.t,d.b);
  const color=avg>=4.5?'var(--green)':avg>=3.5?'var(--gold)':avg>=2.5?'var(--orange)':'var(--red)';
  document.getElementById('scoreDisplay').innerHTML=`
    <div class="score-big" style="color:${color}">${avg}<span style="font-size:0.4em;color:var(--text2)">/5.0</span></div>
    <div class="score-text">四维共振综合确定性评分</div>
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:6px;text-align:center;margin-bottom:16px">
      <div style="background:var(--card2);padding:8px;border-radius:8px">
        <div style="font-size:0.65em;color:var(--text2)">周金涛</div>
        <div style="font-size:1.2em;font-weight:700;color:var(--green)">${d.z}⭐</div>
        <div style="font-size:0.6em;color:var(--text2)">周期定位</div>
      </div>
      <div style="background:var(--card2);padding:8px;border-radius:8px">
        <div style="font-size:0.65em;color:var(--text2)">时寒冰</div>
        <div style="font-size:1.2em;font-weight:700;color:var(--orange)">${d.s}⭐</div>
        <div style="font-size:0.6em;color:var(--text2)">趋势方向</div>
      </div>
      <div style="background:var(--card2);padding:8px;border-radius:8px">
        <div style="font-size:0.65em;color:var(--text2)">宋鸿兵</div>
        <div style="font-size:1.2em;font-weight:700;color:var(--blue)">${d.t}⭐</div>
        <div style="font-size:0.6em;color:var(--text2)">货币环境</div>
      </div>
      <div style="background:var(--card2);padding:8px;border-radius:8px">
        <div style="font-size:0.65em;color:var(--text2)">巴拉塔</div>
        <div style="font-size:1.2em;font-weight:700;color:var(--purple)">${d.b}⭐</div>
        <div style="font-size:0.6em;color:var(--text2)">货币重置</div>
      </div>
    </div>
    <div style="background:var(--card2);padding:14px;border-radius:8px;font-size:0.85em;color:var(--text2);line-height:1.6;border-left:3px solid ${color}">
      <b style="color:var(--text)">📝 四维分析：</b>${d.msg}
    </div>`;
}
// === FAMILIES ===
function initFamilies(){
  const el=document.getElementById('familyList');
  el.innerHTML=families.map(f=>`
    <div class="family-card" onclick="this.querySelector('.family-body').classList.toggle('open')">
      <div class="family-head">
        <div><h3>${f.name}</h3><div style="font-size:0.75em;color:var(--text2);margin-top:2px">${f.country} · ${f.wealth}</div></div>
        <span class="gen">${f.gen}</span>
      </div>
      <div class="family-body">
        <h4 style="color:var(--green);font-size:0.85em;margin-bottom:6px">核心机制</h4>
        <ul>${f.mech.map(m=>`<li>${m}</li>`).join('')}</ul>
        <h4 style="color:var(--orange);font-size:0.85em;margin:10px 0 6px">跨周期策略</h4>
        <p style="font-size:0.82em;color:var(--text2);line-height:1.5">${f.strategy}</p>
      </div>
    </div>`).join('');
}
// === AGE ===
function updateAge(){
  const age=parseInt(document.getElementById('ageSlider').value);
  document.getElementById('ageVal').textContent=age;
  const birthYear=2026-age;
  const el=document.getElementById('ageResult');
  // Timeline
  const tl=document.getElementById('ageTimeline');
  const phases=[
    {label:'五轮萧条',start:2019,end:2030,color:'#1e3a5f'},
    {label:'六轮回升',start:2025,end:2038,color:'#065f46'},
    {label:'六轮繁荣',start:2038,end:2055,color:'#92400e'}
  ];
  const tStart=2019,tEnd=2060;
  tl.innerHTML=phases.map(p=>{
    const left=((p.start-tStart)/(tEnd-tStart)*100);
    const width=((p.end-p.start)/(tEnd-tStart)*100);
    return `<div class="marker" style="left:${left}%;width:${width}%;background:${p.color}">${p.label}</div>`;
  }).join('')+`<div class="you" style="left:${((2026-tStart)/(tEnd-tStart)*100)}%"></div>`;
  // Opportunities
  const opps=[];
  if(age<=35){opps.push({year:'2019',desc:'第二次机会（A股2440点底部）——你当时'+(2026-age<=2019?'尚未成年':'可能错过'),status:2026-age>25?'✅':'⚠️'});}
  opps.push({year:'2026-2028',desc:'播种期定投——AI算力+黄金+小金属，低成本建仓',status:age>=25?'🟢 现在就做':'⏳ 还早'});
  if(age<=45){opps.push({year:'2029-2030',desc:'第三次财富机会（周金涛预测）——核心资产建仓',status:'⭐ 最关键'});}
  if(age<=50){opps.push({year:'2032-2038',desc:'AI应用全面渗透——机器人+产业AI+生物医药',status:'🟢 高回报期'});}
  if(age<=55){opps.push({year:'2038-2045',desc:'第六轮繁荣启动——逐步减持成长股，加仓实物',status:'💰 收获期'});}
  const strategy=age<=30?'进攻型：60%权益+20%实物+15%现金+5%探索':age<=40?'平衡型：50%权益+25%实物+20%固收+5%现金':age<=50?'稳健型：35%权益+30%固收+20%实物+15%现金':'防守型：40%固收+30%权益+20%实物+10%现金';
  const [stype,sdetail]=strategy.split('：');
  el.innerHTML=`
    <div style="background:${age<=35?'#065f4620':age<=45?'#92400e20':'#1e3a5f20'};border:1px solid ${age<=35?'var(--green)':age<=45?'var(--orange)':'var(--blue)'};border-radius:8px;padding:14px;margin-top:16px">
      <div style="font-size:0.8em;color:var(--text2)">你的投资策略</div>
      <div style="font-size:1.1em;font-weight:700;color:${age<=35?'var(--green)':age<=45?'var(--orange)':'var(--blue)'}">${stype}</div>
      <div style="font-size:0.85em;color:var(--text2);margin-top:4px">${sdetail}</div>
    </div>
    <div class="section-title" style="margin-top:16px"><span>⭐</span>你的三次财富机会</div>
    <div class="opp-list">${opps.map(o=>`<div class="opp-item"><div class="opp-year">${o.year}</div><div class="opp-desc">${o.desc} ${o.status}</div></div>`).join('')}</div>
    <div style="margin-top:12px;font-size:0.8em;color:var(--text2);font-style:italic;background:var(--card2);padding:10px;border-radius:8px;border-left:3px solid var(--gold)">
      💡 周金涛忠告："在座各位所经历的第5次康波，你们的人生就是一场康波……你的财富机会完全取决于你对康波周期的理解。"
    </div>`;
}
