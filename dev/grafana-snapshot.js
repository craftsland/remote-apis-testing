const puppeteer = require('puppeteer');

(async () => {

   if (process.argv.length <= 4) {
      console.log("Usage: " + __filename + " <dashboard name> <namespace> <from time (unix ms)> <to time (unix ms)");
      process.exit(-1);
   }

   var userName = 'admin';
   var password = 'admin';
   var baseUrl = 'http://127.0.0.1:3000/d/'

   var dashboardName = process.argv[2];
   var nameSpace = process.argv[3];
   var fromTime = process.argv[4];
   var toTime = process.argv[5];

   // Launch headless browser
   const browser = await puppeteer.launch({args: ['--no-sandbox', '--disable-setuid-sandbox']});

   // Open login page - assumes we have port forwarded to the kubernetes grafana port
   const page = await browser.newPage();
   await page.goto('http://127.0.0.1:3000/login');
   
   // Proceed to log in, as we start from clean admin:admin credentials we are presented with a change password screen
   // Bypass that by using the skip option
   if (page!==null){
      await page.screenshot({path: 'dashboard-1.png'});
      await page.type('[name="username"]', userName, { delay: 100 });
      await page.type('[id="inputPassword"]', password, { delay: 100 });
      await page.click('[type="submit"]');
      await page.waitFor(1000);
      await page.screenshot({path: 'dashboard-2.png'});
      await page.type('[name="confirmNew"]', "vgrade", { delay: 100 });
      await page.type('[id="newPassword"]', "vgrade", { delay: 100 });
      await page.screenshot({path: 'dashboard-3.png'});
      await page.click('[ng-click="skip();"]');
      await page.waitForNavigation({waitUntil: 'networkidle2'});
   }   

   // Open a new page to the required dashboard, namespace and time interval passed in from the commandline
   // eg node grafana-snapshot.js kubernetes-compute-resources-namespace-pods buildbarn 1565180677000 1565181677000
   await page.goto(baseUrl+
	           dashboardName+
	           '?orgId=1&var-datasource=prometheus&var-cluster='+
	           '&var-namespace='+
	           nameSpace+
	           '&from='+
	           fromTime+
	           '&to='+
	           toTime,
	           {waitUntil: 'networkidle2'});

   
   if (dashboardName == '85a562078cdf77779eaa1add43ccec1e/kubernetes-compute-resources-namespace-pods') {

      // Close quota tabs 
   
      await page.waitForSelector('.react-grid-layout > #panel-6 > .dashboard-row > .dashboard-row__title > .fa')
      await page.click('.react-grid-layout > #panel-6 > .dashboard-row > .dashboard-row__title > .fa')
   
      await page.waitForSelector('.react-grid-layout > #panel-8 > .dashboard-row > .dashboard-row__title > .fa')
      await page.click('.react-grid-layout > #panel-8 > .dashboard-row > .dashboard-row__title > .fa')

   };

   await page.screenshot({path: 'dashboard-4.png'});

   // Create pdf of dashboard	
   await page.pdf({
                  path: 'dashboard.pdf',
                  format: 'A3',
                  scale: 0.75,
                  displayHeaderFooter: false,
                  printBackground: false,
                  margin: {
                          top: 0,
                          right: 0,
                          bottom: 0,
                          left: 0,
                  },
   });

   // Share dashboard to external service, eg, https://snapshot.raintank.io/dashboard/snapshot/segDK0PQbGTt0css3x4AmwBwiqBiiSNL 

   // Click navbar share button and wait for share dialog 
   page.click('[class="btn navbar-button navbar-button--share"]');
   await page.waitForSelector('a[class="gf-tabs-link"]');
   
   // Click on link tab and wait for create snapshot button
   page.click('a[class="gf-tabs-link"]');
   await page.waitForSelector('[ng-click="createSnapshot(true)"]');
   
   // Click snapshot button and wait for snapshot link to be displayed
   page.click('[ng-click="createSnapshot(true)"]');
   await page.waitForSelector('a[class="large share-modal-link"]');
   
   // Harvest snapshot link
   let href = await page.$eval('a[class="large share-modal-link"]', a => a.href)
   
   // Print snapshot link to console
   console.log(href);

   await browser.close();
})();

