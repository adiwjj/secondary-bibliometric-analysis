"""Figures for the paper (Figures 2, 3B, 4 and 5). Run after layers A to D."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import TABLES, FIGURES, VOS_NETWORK
import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8.5,'axes.spines.top':False,'axes.spines.right':False,
 'axes.edgecolor':'#4a4a4a','axes.labelcolor':'#0b0b0b','xtick.color':'#1a1a1a','ytick.color':'#1a1a1a'})
BLUE='#2a78d6'; ORANGE='#eb6834'; GREY='#a9a8a2'; INK='#0b0b0b'; INK2='#262626'
m=pd.read_csv(TABLES/'layerA_keywords.csv').rename(columns={'category':'cat','occurrences':'occ'}); n=pd.read_csv(VOS_NETWORK,sep='\t',header=None,names=['a','b','w'])
pos={r.id:(r.x,r.y) for r in m.itertuples()}; lab=dict(zip(m.id,m.label)); cat=dict(zip(m.id,m.cat))
OFF={'social determinants of health':(0.2,-0.115),'social inequality':(0.07,0),'rural broadband':(-0.04,0)}
# ---------- Fig 2 network
fig,ax=plt.subplots(figsize=(7.2,5.0))
for r in n.itertuples():
    h = cat[r.a]=='Health' or cat[r.b]=='Health'
    (x1,y1),(x2,y2)=pos[r.a],pos[r.b]
    ax.plot([x1,x2],[y1,y2],color=ORANGE if h else '#d6d5d0',lw=0.6+0.55*r.w,alpha=0.75 if h else 0.6,zorder=1 if not h else 2)
for r in m.itertuples():
    h=r.cat=='Health'; x,y=pos[r.id]
    ax.scatter(x,y,s=25+16*r.occ,color=ORANGE if h else GREY,edgecolor='white',linewidth=1.2,zorder=3)
    dx,dy=OFF.get(r.label,(0,0))
    ax.text(x+dx,y+0.045+0.0035*r.occ+dy,r.label,ha='center',va='bottom',fontsize=7.3 if not h else 8,
            color=INK if h else INK2,fontweight='bold' if h else 'normal',zorder=4)
ax.set_axis_off()
from matplotlib.lines import Line2D
ax.legend(handles=[Line2D([],[],marker='o',ls='',color=ORANGE,label='Health-related keyword (n = 7)'),
                   Line2D([],[],marker='o',ls='',color=GREY,label='Other keyword (n = 30)'),
                   Line2D([],[],color=ORANGE,lw=1.5,label='Link incident to a health keyword')],
          loc='upper center',bbox_to_anchor=(0.5,0.0),ncol=3,frameon=False,fontsize=7.5)
plt.tight_layout(); plt.savefig(FIGURES/'fig3b_network_health_links.png',dpi=300); plt.close()
# ---------- Fig 3 heatmap
AS=pd.read_csv(TABLES/'layerC_association_strength.csv',index_col=0); CO=pd.read_csv(TABLES/'layerC_cooccurrence.csv',index_col=0)
rows=['Telemedicine and telehealth','Digital health and mHealth','Healthcare access and services','Health equity and disparities','Health literacy','Social determinants of health','Chronic disease management','Mental health and well-being','Pandemic (COVID-19)']
AS=AS.loc[rows]; CO=CO.loc[rows]
fig,ax=plt.subplots(figsize=(7.2,4.3))
from matplotlib.colors import LinearSegmentedColormap, TwoSlopeNorm
cmap=LinearSegmentedColormap.from_list('d',['#5b8fd0','#f2f1ed','#d9572a'])
im=ax.imshow(np.log2(AS.values.astype(float)),cmap=cmap,norm=TwoSlopeNorm(0,-1.8,2.8),aspect='auto')
for i in range(AS.shape[0]):
    for j in range(AS.shape[1]):
        v=AS.values[i,j]; c=int(CO.values[i,j])
        ax.text(j,i,f'{v:.2f}\n(n={c})',ha='center',va='center',fontsize=6.6,color=INK)
ax.set_xticks(range(AS.shape[1])); ax.set_xticklabels(AS.columns,fontsize=7,rotation=30,ha='right')
ax.set_yticks(range(AS.shape[0])); ax.set_yticklabels(rows,fontsize=7.5)
ax.tick_params(length=0); [s.set_visible(False) for s in ax.spines.values()]
ax.set_xticks(np.arange(-.5,AS.shape[1]),minor=True); ax.set_yticks(np.arange(-.5,AS.shape[0]),minor=True)
ax.grid(which='minor',color='white',lw=2); ax.tick_params(which='minor',length=0)
cb=plt.colorbar(im,ax=ax,fraction=0.03,pad=0.02); cb.set_ticks(np.log2([0.5,1,2,4])); cb.set_ticklabels(['0.5','1 (expected)','2','4'])
cb.set_label('Association strength (observed/expected, log scale)',fontsize=7); cb.outline.set_visible(False); cb.ax.tick_params(labelsize=7)
plt.tight_layout(); plt.savefig(FIGURES/'fig4_association_heatmap.png',dpi=300); plt.close()
# ---------- Fig 4 temporal
y=pd.read_csv(TABLES/'layerD_yearly.csv').rename(columns={'share_pct':'share'}); tab=pd.read_csv(TABLES/'layerD_concepts_by_period.csv',index_col=0)
fig=plt.figure(figsize=(7.2,5.6))
top,bot=fig.subfigures(2,1,height_ratios=[1,1.1],hspace=0.06)
ax,ax2=top.subplots(1,2,gridspec_kw={'wspace':0.28})
top.subplots_adjust(left=0.08,right=0.98,bottom=0.13,top=0.88)
ax.bar(y.Year,y.health,color=BLUE,width=0.7,label='Health-oriented articles')
ax.bar(y.Year,y.total-y.health,bottom=y.health,color=GREY,width=0.7,edgecolor='white',linewidth=1,label='Other articles')
ax.set_title('(A) Annual articles',loc='left',fontsize=8.5,color=INK)
ax.set_ylabel('Articles'); ax.set_xticks(range(2015,2027,2)); ax.legend(frameon=False,fontsize=7,loc='upper left')
ax.yaxis.grid(True,color='#ecebe7'); ax.set_axisbelow(True)
ax2.plot(y.Year,y.share,color=BLUE,lw=2,marker='o',ms=4,markeredgecolor='white')
_p=pd.read_csv(TABLES/'layerD_periods.csv',index_col=0)['share_pct']; per={k.replace('-','–'):round(v,1) for k,v in _p.items()}; spans=[(2015,2020),(2021,2023),(2024,2026)]
for (a_,b_),(k,v) in zip(spans,per.items()):
    ax2.hlines(v,a_-0.3,b_+0.3,color=ORANGE,lw=1.6,ls='--'); ax2.text((a_+b_)/2,v+2.2,f'{v:.1f}%',ha='center',fontsize=7,color=INK2)
ax2.set_title('(B) Share of health-oriented articles (%)',loc='left',fontsize=8.5,color=INK)
ax2.set_ylim(0,48); ax2.set_xticks(range(2015,2027,2)); ax2.yaxis.grid(True,color='#ecebe7'); ax2.set_axisbelow(True)
ax2.text(2015,44,'Dashed line = period mean',fontsize=6.8,color=INK2)
ax3=bot.subplots(); bot.subplots_adjust(left=0.30,right=0.98,bottom=0.17,top=0.92)
order=tab.sum(axis=1).sort_values().index; tab=tab.loc[order]
import matplotlib.cm as cm
cols=[matplotlib.colors.to_hex(cm.viridis(v)) for v in (0.22,0.58,0.92)]; h=0.26
for k,(c,col) in enumerate(zip(tab.columns,cols)):
    ax3.barh(np.arange(len(tab))+(k-1)*h,tab[c],height=h-0.03,color=col,label=c.replace('-','–'))
ax3.set_yticks(range(len(tab))); ax3.set_yticklabels(tab.index,fontsize=7.5)
ax3.set_xlabel('Health-oriented articles addressing the theme'); ax3.legend(frameon=False,fontsize=7,loc='lower right',title='Period',title_fontsize=7)
ax3.set_title('(C) Health themes by publication period',loc='left',fontsize=8.5,color=INK)
ax3.xaxis.grid(True,color='#ecebe7'); ax3.set_axisbelow(True)
plt.savefig(FIGURES/'fig5_temporal.png',dpi=300); plt.close()
# ---------- Fig 1 workflow
fig,ax=plt.subplots(figsize=(7.2,3.0)); ax.set_xlim(0,100); ax.set_ylim(0,44); ax.axis('off')
def box(x,y,w,hh,t,fc,ec,fs=7,bold=False):
    ax.add_patch(FancyBboxPatch((x,y),w,hh,boxstyle='round,pad=0.3,rounding_size=1.0',fc=fc,ec=ec,lw=1))
    ax.text(x+w/2,y+hh/2,t,ha='center',va='center',fontsize=fs,color=INK,fontweight='bold' if bold else 'normal',linespacing=1.3)
box(0.5,14,15,14,'Existing corpus\n(Paper 1)\n596 articles\nLens.org\n2015–2026','#f2f1ed','#8a8984',fs=6.6)
L=[('Layer A\nKeyword\nnetwork','37 keywords\n(threshold 2)\n7 health seeds\nlink strength,\nbetweenness','RQ1, RQ2'),
   ('Layer B\nSub-corpus\nextraction','Health dictionary\ntitles, keywords,\nMeSH, abstracts\n→ 85 health-\noriented articles','RQ1'),
   ('Layer C\nConcept\nco-occurrence','9 health × 8\nconnectivity\nconcepts; six\nUMC dimensions','RQ2'),
   ('Layer D\nTemporal\nanalysis','Annual share,\nthree publication\nperiods, overlay\naverage year','RQ3')]
for i,(a,b,rq) in enumerate(L):
    x=21+i*20; w=17
    box(x,27,w,11,a,'#e3eefb',BLUE,fs=7,bold=True)
    box(x,1,w,20,b,'white','#c3c2b7',fs=6.4)
    ax.annotate('',xy=(x+w/2,21.6),xytext=(x+w/2,26.4),arrowprops=dict(arrowstyle='-|>',color=INK2,lw=0.8))
    ax.text(x+w/2,41.2,rq,ha='center',fontsize=7,color=ORANGE,fontweight='bold')
    if i<3: ax.annotate('',xy=(x+w+2.6,32.5),xytext=(x+w+0.5,32.5),arrowprops=dict(arrowstyle='-|>',color=INK2,lw=0.8))
ax.annotate('',xy=(20.4,32.5),xytext=(15.9,24),arrowprops=dict(arrowstyle='-|>',color=INK2,lw=0.9))
plt.savefig(FIGURES/'fig2_workflow.png',dpi=300,bbox_inches='tight'); plt.close()
