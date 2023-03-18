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

// LongMin (XMin) LongMax (XMax) LatMin(YMin) LatMax(YMax)
const LongLatMaxMin = [180,-180,90,-90]
const imageWidth = 900; //px   
const imageHeight = 750; //px
const LongLatWidth = LongLatMaxMin[0] - LongLatMaxMin[1] // 360 - Longitude is X
const LongLatHeight = LongLatMaxMin[2] - LongLatMaxMin[3] // 180 - Latitude is Y


function convert([long,lat]){

    width = (long-LongLatMaxMin[0])/LongLatWidth
    height = (lat-LongLatMaxMin[2])/LongLatHeight
    x = Math.floor(imageWidth * width)
    y = Math.floor(imageHeight * (1-height))
    cood = [x,y]
    return cood;
}

//Reference https://towardsdatascience.com/geotiff-coordinate-querying-with-javascript-5e6caaaf88cf