// Define our labelmap
export const labelMap = {
    1:{name:'person without helmet', color:'red',Violated:"Hard hat"},
    2:{name:'person with helmet', color:'green',Violated:"No Object Violated"},

}

// Define a drawing function
export const drawRect = (boxes, classes, scores, threshold, imgWidth, imgHeight, ctx)=>{
    for(let i=0; i<=boxes.length; i++){
        if(boxes[i] && classes[i] && scores[i]>threshold){
            // Extract variables
            const [y,x,width,height] = boxes[i]
            const text = classes[i]
            
            // Set styling
            ctx.strokeStyle = labelMap[text]['color']
            ctx.lineWidth = 5
            ctx.fillStyle = 'white'
            ctx.font = '20px Arial'         
            
            // DRAW!!
            ctx.beginPath()
            ctx.fillText(labelMap[text]['name'] + ' - ' + Math.round(scores[i]*100)/100, x*imgWidth, y*imgHeight-10)
            ctx.rect(x*imgWidth, y*imgHeight, width*imgWidth/2, height*imgHeight/1.5);
            ctx.stroke()
        }
    }
}