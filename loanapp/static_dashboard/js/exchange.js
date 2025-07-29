/* 
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/JSP_Servlet/JavaScript.js to edit this template
 */

function numberWithSpaces(x) {
    ans = x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
    //console.log("ans: "+ans);
    return ans;
}

function exchange(myrates,todo,fromamount,fromcurr,tocurr,fromrate,torate) {
    // values for todo: curr,send,myrate
    let send = 0;
    let fromratelocal = 1;
    let toratelocal = 1;
    let gets = 0;
    let ans;
    
    if(todo === 'curr') {
        // calc rate and recipientGets
        send = fromamount;
        fromratelocal = (myrates[tocurr] / myrates[fromcurr]).toFixed(8);
        toratelocal = (myrates[fromcurr] / myrates[tocurr]).toFixed(8);        
        gets = (fromamount * fromratelocal).toFixed(2);
    }
    else if(todo === 'send') {
        // calc gets
        send = fromamount;
        fromratelocal = fromrate;
        toratelocal = torate;
        gets = (fromamount * fromratelocal).toFixed(2);
    }
    else if(todo === 'xrate') {
        // calc gets
        send = fromamount;
        fromratelocal = fromrate;
        toratelocal = (1/fromrate).toFixed(8);
        gets = (fromamount * fromratelocal).toFixed(2);
    }
    
    ans = {
        send: send,
        fromratelocal: fromratelocal,
        fromratelocalFmt: "or "+fromratelocal+" "+tocurr+" per "+fromcurr,
        toratelocal: toratelocal,
        toratelocalFmt: "or "+toratelocal+" "+fromcurr+" per "+tocurr,
        gets: gets,
        getsFmt: numberWithSpaces(gets)+" "+tocurr
    };
    
    return ans;
}