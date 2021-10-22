/**
 * There is a large pile of socks that must be paired by color.
 * Given an array of integers representing the color of each sock.
 * determine how many pairs of socks with matching colors there are.
 * 
 * Ex:
 * INPUTS:
 *      n = 7
 *      ar = [1,2,1,2,1,3,2]
 * OUTPUT:
 *      result = 2
 * Solution: 
 *      There is one pair of color 1 and one of color 2.
 *      There are three odd socks left, one of each color.
 *      The number of pairs is 2.
 * 
 * My Solution:
 *  1. make to pointers ==> one is for the first color 
 *                      ==> second is the other colors (lopping through all array)
 * 
 *  2. if we find a pair: ==> remove two of them from the array
 *                        ==> add +1 to the _result_
 *                        ==> change the the  first pointer to the next element of array
 *                        ==> repeat the first step until the second pointer acheave to th last element of array
 * 
 */

 // n = 10
 // ar = [1,1,3,1,2,1,3,3,3,3]
 //       0 1 2 3 4 5 6 7 8 9

 function sockMerchant(n, ar) {
    let result = 0
    for(let i=0; i<ar.length; i++){
        let pointer_1 = ar[i]
        for(let j=i+1; j<ar.length-1; j++){
            let pointer_2 = ar[j]
            if(pointer_1 == pointer_2){
                result += 1
                ar.splice(i, 1)
                ar.splice(j, 1)
                break;
            }
        }
    }
}



 function sockMerchant(n, ar) {
    let new_arr = ar // new_arr = [1,1,3,1,2,1,3,3,3,3] [1,4,3,1,2,1,3,3,3,3]
    let result = 0
    for(let i=0; i<ar.length; i++){ // i = 3
        let k = 0
        let pointer_1 = new_arr[k] // pointer_1 = 3
        for(let j=i+1; j<new_arr.length; j++){ // j = 6
            k += 1
            let pointer_2 = new_arr[k] // pointer_2 = 3
            if(pointer_1 === pointer_2){ // 
                new_arr.splice(i, 1)
                new_arr.splice(j, 1)
                result += 1
                break;
                // new_arr = [3,1,2,1,3,3,3,3]
            }
        }
    }
    // ar = [1,1,3,1,2,1,3,3,3,3]
    return result // result = 2
}


// n = 10
 // ar = [1,1,3,1,2,1,3,3,3,3]
 //       0 1 2 3 4 5 6 7 8 9
 function sockMerchant(n, ar) {
    let new_arr = ar 
    let result = 0
    for(let i=0; i<ar.length; i++){ // i = 6<0    __ length = 1
        let k = 0
        let pointer_1 = new_arr[0] // pointer_1 = 3
        if(new_arr.includes(pointer_1, 1) ){
            for(let j=i+1; j<new_arr.length; j++){ // j = 5    __ length = 1
                k += 1    // k = 1
                let pointer_2 = new_arr[k] // pointer_2 = 3
                if(pointer_1 === pointer_2){ // 
                    new_arr.splice(k, 1)
                    new_arr.splice(0, 1)
                    result += 1
                    break;
                }
            }// new_arr = []
        }else{
            new_arr.splice(0, 1)
        }
        }
        
    // ar = [1,1,3,1,2,1,3,3,3,3]
    return result // result = 4
}



// n = 10
 // ar = [1,1,3,1,2,1,3,3,3,3]
 //       0 1 2 3 4 5 6 7 8 9
 function sockMerchant(n, ar) {
    let new_arr = ar 
    let result = 0
    let i = 0
    while(i<ar.length && new_arr.length != 0){
        i += 1
        let k = 0
        let pointer_1 = new_arr[0] // pointer_1 = 3
        if(new_arr.includes(pointer_1, 1) ){
            for(let j=i+1; j<new_arr.length; j++){ // j = 5    __ length = 1
                k += 1    // k = 1
                let pointer_2 = new_arr[k] // pointer_2 = 3
                if(pointer_1 === pointer_2){ // 
                    new_arr.splice(k, 1)
                    new_arr.splice(0, 1)
                    result += 1
                    break;
                }
            }// new_arr = []
        }else{
            new_arr.splice(0, 1)
        }
    }
    
        
    // ar = [1,1,3,1,2,1,3,3,3,3]
    return result // result = 4
}




function sockMerchant(n, ar) {
    var res = 0;
        ar.sort();
        for(let i=0; i<n;i++){
            if(ar[i] == ar[i+1]){
                i++;
                      res++;
               }
        }
    return res;
    }