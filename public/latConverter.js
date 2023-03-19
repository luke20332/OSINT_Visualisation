function covert([lat, long]) {
    R = 6378137; //radius of earth in m

    rad_lat = lat * Math.PI/180;
    rad_long = long * Math.pi/180;

    x = R * rad_long;
    y = R * Math.log((Math.tan((Math.pi)/4)+(((Math.pi/2)-rad_lat)/2)));

    ans = [x, y]
    console.log("function was called and the answer is: " + ans)
    return ans;
}

// [minLong, minLat, maxLong, maxLat];
var minLong = -85;
var minLat = -90;
var maxLong = 85;
var maxLat = 90;
var bbox = [minLong, minLat, maxLong, maxLat];
var pixelWidth = 350;
var pixelHeight = 350;
var bboxWidth = bbox[2] - bbox[0];
var bboxHeight = bbox[3] - bbox[1];

var convertToXY = function(latitude, longitude) {
    var widthPct = ( longitude - bbox[0] ) / bboxWidth;
    var heightPct = ( latitude - bbox[1] ) / bboxHeight;
    var x = Math.floor( pixelWidth * widthPct );
    var y = Math.floor( pixelHeight * ( 1 - heightPct ) );
    return { x, y };
}
//Reference https://towardsdatascience.com/geotiff-coordinate-querying-with-javascript-5e6caaaf88cf
//Reference https://stackoverflow.com/questions/14329691/convert-latitude-longitude-point-to-a-pixels-x-y-on-mercator-projection


//TODO
//https://gis.stackexchange.com/questions/23321/where-can-i-download-a-good-world-image-in-geotiff
//Check uploaded images