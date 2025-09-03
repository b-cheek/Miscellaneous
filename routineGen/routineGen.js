
const abcjs = window.ABCJS;

const weightedSelectionList = (allWeightsObj, options = [], bagSize = -1) => {
    list = [];
    const weightsObj = (options == []) 
        ? Object.keys(allWeightsObj).filter(k => options.includes(k))
            .reduce((obj, key) => {
                obj[key] = allWeightsObj[key];
                return obj;
            }, {})
        : allWeightsObj;
    sizeModifier = (bagSize > 0) 
        ? bagSize/Object.values(weightsObj).reduce((a, b) => a + b, 0)
        : 1
        
    for (let key in weightsObj) {
        list.push(...Array(Math.floor(weightsObj[key]*sizeModifier)).fill(key))
    }
    return list
}

const randomArraySelect = (array) => array[Math.floor(Math.random() * array.length)];

const marbleRandomArraySelect = (array) => array.pop(Math.floor(Math.random() * array.length));

// Easy to combine but may want to only make weighted selection list once to lighten computational load
// or allow for marble bag technique
const randomWeightChoice = (weightsObj, options = []) => randomArraySelect(weightedSelectionList(weightsObj, options));

const generateRoutine = () => {

    // scaleWeights = weightedSelectionList(routineWeights["sequence routine"]["small jump"]["scale"]);

    for (let i = 0; i<1; i++) {

        let smallJumpIntervals;

        const smallJumpScale = randomWeightChoice(routineWeights["sequence routine"]["small jump"]["scale"]);
        
        switch(smallJumpScale) {
            case "major":
                smallJumpIntervals = 2, 2, 1, 2, 2, 2, 1;
                break;
            case "minor":
                smallJumpIntervals = 2, 1, 2, 2, 1, 2, 2; 
                break;
            case "harmonic minor":
                smallJumpIntervals = 2, 1, 2, 2, 1, 3, 1;
                break;
            case "melodic minor":
                break;
        }

        const smallJumpScaleOptions = routineWeights["sequence routine"]["small jump"]["harmonic options"][smallJumpScale];

        const smallJumpPattern = (smallJumpScale, randomWeightChoice(routineWeights["sequence routine"]["small jump"]["harmonic pattern"], smallJumpScaleOptions));
        
        const smallJumpArticulationPattern = (randomWeightChoice(routineWeights["sequence routine"]["articulation pattern"][
            (routineWeights["sequence routine"]["three note patterns"].includes(smallJumpPattern)
            ? "base 3"
            : "base 2")
        ]))

        const smallJumpArticulationStyle = randomWeightChoice(routineWeights["sequence routine"]["articulation style"])

        let dynamicSpeed = randomWeightChoice(routineWeights["sequence routine"]["dynamic pattern"]["speed"]);

        let dynamicBlocks = ""

        for (let i=0; i<parseInt(randomWeightChoice(routineWeights["sequence routine"]["dynamic pattern"]["blocks"])); i++) {
            dynamicBlocks += randomWeightChoice(routineWeights["sequence routine"]["dynamic pattern"]["dynamics"]) + ",";
        }

        console.log(`${smallJumpScale} ${smallJumpPattern}, ${smallJumpArticulationPattern} ${smallJumpArticulationStyle}, ${dynamicSpeed}, ${dynamicBlocks}`)

        let bigJumpIntervals;

        const bigJumpScale = randomWeightChoice(routineWeights["sequence routine"]["small jump"]["scale"]);
        
        switch(smallJumpScale) {
            case "major":
                bigJumpIntervals = 2, 2, 1, 2, 2, 2, 1;
                break;
            case "minor":
                bigJumpIntervals = 2, 1, 2, 2, 1, 2, 2; 
                break;
            case "harmonic minor":
                bigJumpIntervals = 2, 1, 2, 2, 1, 3, 1;
                break;
            case "melodic minor":
                break;
        }

        const bigJumpScaleOptions = routineWeights["sequence routine"]["big jump"]["harmonic options"][bigJumpScale];

        const bigJumpPattern = (bigJumpScale, randomWeightChoice(routineWeights["sequence routine"]["big jump"]["harmonic pattern"], bigJumpScaleOptions));
        
        const bigJumpArticulationPattern = (randomWeightChoice(routineWeights["sequence routine"]["articulation pattern"][
            (routineWeights["sequence routine"]["three note patterns"].includes(bigJumpPattern)
            ? "base 3"
            : "base 2")
        ]))

        const bigJumpArticulationStyle = randomWeightChoice(routineWeights["sequence routine"]["articulation style"])

        dynamicSpeed = randomWeightChoice(routineWeights["sequence routine"]["dynamic pattern"]["speed"]);

        dynamicBlocks = ""

        for (let i=0; i<parseInt(randomWeightChoice(routineWeights["sequence routine"]["dynamic pattern"]["blocks"])); i++) {
            dynamicBlocks += randomWeightChoice(routineWeights["sequence routine"]["dynamic pattern"]["dynamics"]) + ",";
        }

        console.log(`${bigJumpScale} ${bigJumpPattern}, ${bigJumpArticulationPattern} ${bigJumpArticulationStyle}, ${dynamicSpeed} ${dynamicBlocks}`)

        

        randomWeightChoice(routineWeights["sequence routine"]["dynamic pattern"]["speed"]);
        randomWeightChoice(routineWeights["sequence routine"]["dynamic pattern"]["blocks"]);
        randomWeightChoice(routineWeights["sequence routine"]["dynamic pattern"]["dynamics"]);

        randomWeightChoice(routineWeights["sequence routine"]["articulation pattern"]["base 2"]);
        randomWeightChoice(routineWeights["sequence routine"]["articulation pattern"]["base 3"]);
        randomWeightChoice(routineWeights["sequence routine"]["articulation style"]);
        
        // console.log([...scaleWeights])
        // console.log(marbleRandomArraySelect(scaleWeights));
    }



    abcjs.renderAbc("paper", '');
}
