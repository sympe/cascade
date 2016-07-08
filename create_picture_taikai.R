
library(RColorBrewer)

file1.name<-sprintf("../pic_csv/attack_target.csv")
# file2.name<-sprintf("./pic_csv/attack50_deg.csv")
# file3.name<-sprintf("./pic_csv/attack50_close.csv")
# file4.name<-sprintf("./pic_csv/attack50_page.csv")
# file5.name<-sprintf("./pic_csv/attack50_ci.csv")
# file6.name<-sprintf("./pic_csv/attack50_random.csv")

x.label<-expression(paste("Tolerance ",alpha))
y.label<-("Fraction of nodes")

#######################
#
#  "pic_csv/attack_random.csv"
#
#######################

data1<-read.csv(file1.name, header=T)

pch <- c(1, 2, 3) # 点の形
cols <- brewer.pal(9, "Set1")
col <- c(cols[1], cols[2], cols[3]) # 線の色
#rain <- rainbow(12)
#col <- c(rain[2], rain[4], rain[6], rain[8], rain[10], rain[12]) # 線の色
#labels<-colnames(data1)[-1] # 線の名前
labels<- c("Giant component\n(Uniform traffic)", "Giant component\n(Traffic to sink)", "Component with sink\n(Traffic to sink)")

d<-data1[,1]
uni<-data1[,2]
sinkgc<-data1[,3]
sinkph<-data1[,4]

pdf(file="../picture/target.pdf", width=7, height=6, pointsize=27)
par(mgp=c(1.5,0.5,0), mar=c(2.4,3,0.5,1))
plot(d, uni, xlim=c(1,50),ylim=c(0,1), pch=pch[1], col=col[1], lty=1, lwd=2, type="o", yaxp=c(0,1,10),
	xlab=x.label, ylab=y.label)
axis(side=1, at=c(2))
points(d, sinkgc, pch=pch[2], col=col[2], type="o", lty=1, lwd=2)
points(d, sinkph, pch=pch[3], col=col[3], type="o", lty=1, lwd=2)
legend("bottomright", legend = labels, col = col, pch = pch, lwd=2, bty="n", cex = 0.8, x.intersp = 0.75, y.intersp = 1.7)
dev.off()