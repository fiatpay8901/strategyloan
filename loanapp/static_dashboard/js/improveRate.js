/* 
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/JSP_Servlet/JavaScript.js to edit this template
 */

function improveRate(curr, rate) {
    if (curr === "BOB") {
        //console.log("rate: "+rate);
        let ans = Number(rate)+8.50;
        ans = 13.00;
        
        //console.log("ans: "+ans);
        return ans;
    }
    else {
        return rate;
    }
}
