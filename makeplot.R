#setwd('~/tmonitor2')
options(stringsAsFactors=FALSE)
today <- as.Date(format(Sys.time(), format="%Y-%m-%d %H:%M:%S", tz="America/New_York"))
print(today)

todaysfile <- paste0(today, '.csv')
dat <- read.csv(todaysfile)
dat$Time <- as.POSIXct(dat$Time)
timeint <- round(dat[-1,'Time']-dat[-nrow(dat),'Time']) > 11
timeoff <- which(timeint)
minmax <- range(dat[,c(1,2)])
avg <- mean(minmax)
legloc <- switch(as.numeric(dat[nrow(dat), 's1'] >= avg) + 1, 'topright', 'bottomright')
bl <- rgb(0,0,1,.4)

png('plot.png', height=400, width=600)
    plot(s1 ~ Time, dat, xaxt = "n", type = "l", main=today, ylim=minmax, ylab="Fahrenheit")
    lines(s2 ~ Time, dat, col=bl)
    if(length(timeoff)) {
        for(x in timeoff) {
            xs <- dat[c(x, x+1, x+1, x),'Time']
            y2 <- c(dat[c(x, x+1),'s2'], 0, 0)
            polygon(x=xs, y=y2, border=NA, col=rgb(.1, 0, .7, 0.4))
            y1 <- c(dat[c(x, x+1), 's1'], 0, 0)
            polygon(x=xs, y=y1, border=NA, col=rgb(.7, 0, 0, 1))
        }
    }
    legend(legloc, legend=c('sensor 1', 'sensor 2'), col=c('black', bl), lty=1, bty='n')
    title(paste("Last record at:", dat[nrow(dat), 'Time']), line=0.5, cex.main=0.9)
    xax <- pretty(dat$Time)
    axis(1, xax, format(as.POSIXct(xax, origin="1970-01-01"), "%H:%M"), cex.axis = .7, las=2)
dev.off()
