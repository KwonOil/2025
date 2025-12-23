let images = [
    "https://i.namu.wiki/i/GoalUYaLUb87TJTBQ3OElqI271xO3OikIISGLEmtE_q7sX8d-OCBzadpr_dUhjfCUq2FcZAzUcaXWrosEFpbf3PBXRI73-kiUCCmjO6acuaACpullzKlwXS1dQ9Hww7Ww5j70i1UBagwZ1S5WIvHKg.webp",
    "https://t1.kakaocdn.net/thumb/R1920x0.fwebp.q100/?fname=https%3A%2F%2Ft1.kakaocdn.net%2Fkakaocorp%2Fkakaocorp%2Fadmin%2Fservice%2Fa85d0594017900001.jpg",
    "https://i.namu.wiki/i/c5LYw4LiYhly3ldzqoPJ6e9nf1QBuNDn-t3Vjo_rLLm6erQtm_Ndx8D7PbqqMae_Azk4RfSxGENFkDBPkmdRJirEqejQ3siVFCwwf4f0LckWzxclPqMPCrFG26WekGImYjocg402fjivqfTnEHS4ww.webp"
];
// let second = 1;

// setInterval(function(){
//     $("img[alt = 'kakao']").attr({
//             "src":images[second]
//         });
//     second++;
//     if(second >= images.length){
//         second = 0;
//     }
// }, 2000);

$("button").on("click", function() {
    let imgIndex = parseInt($(this).attr("id")) - 1;
    let imgName = images[imgIndex];
    $("img[alt = 'kakao']").attr({
        "src" : imgName
    });
});
