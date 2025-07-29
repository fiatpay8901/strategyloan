/* 
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/ClientSide/javascript.js to edit this template
 */

function calcLocalDate(value) {
    var dodebug = false;
    //
    if (dodebug) console.log("debug calcLocalDate");
    let xdateObj = new Date(value);
    let xdate = xdateObj.toDateString();
    let xtime = xdateObj.toTimeString().substring(0,8);
    //
    let xdateShortSplit = xdate.split(" ");
    let xdateShort = "err";
    if (dodebug) console.log(xdate);
    if (dodebug) console.log(xdateShortSplit.length);
    if(xdateShortSplit.length === 4) {
        xdateShort = xdateShortSplit[1]+" "+xdateShortSplit[2]+" "+xdateShortSplit[3];
    }
    const xstampArr = [xdate,xtime,xdateShort];
    
    /*
    console.log(xdate);
    console.log(xtime);
    console.log(xstampArr);
     * 
     */
    return (xstampArr);
}