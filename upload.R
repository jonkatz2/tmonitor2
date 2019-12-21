.libPaths(c("/home/pi/R/armv6l-unknown-linux-gnueabihf-library/3.6","/usr/local/lib/R/site-library","/usr/local/lib/R/library"))

library(RMariaDB)
con <- RMariaDB::dbConnect(
	drv = MariaDB(),
    dbname = "hrrc_1",
	user = "admin100", 
	password = "LawnCloudyWindow", 
	host = "decisionsr-1.cghjyqj3cj4o.us-east-1.rds.amazonaws.com",
	port = 3306
)
options(stringsAsFactors=FALSE)
today <- as.Date(format(Sys.time(), format="%Y-%m-%d %H:%M:%S", tz="America/New_York"))
print(today)

dat <- read.csv('temperatures.csv')
vals <- unlist(lapply(1:nrow(dat), function(x) { 
    paste0("(NULL,", dat[x,"s1"], ",", dat[x,"s2"], ",", dat[x,"s3"], ",", dat[x,"s4"], ",'", dat[x,"Time"], "')")
}))
vals <- paste0(vals, collapse=",")
r <- dbExecute(con, paste0("INSERT INTO tblTemp VALUES ", vals, ";"))
if(r) {
    dat <- dat[-c(1:nrow(dat)),]
    write.csv(dat, 'temperatures.csv', row.names=FALSE)
}

