function covert([lat, long]) {
    R = 6378137; //radius of earth in m

    rad_lat = lat * Math.PI/180;
    rad_long = long * Math.pi/180;

    x = R * rad_long;
    y = R * Math.log((Math.tan((Math.pi)/4)+(((math.pi/2)-rad_lat)/2)));

    ans = [x, y]
    console.log("function was called and the answer is: " + ans)
    return ans;
}