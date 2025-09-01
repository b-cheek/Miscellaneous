
const abcjs = window.ABCJS;

const weightedSelectionList = (weightsObj, bagSize = -1) => {
    list = []
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
const randomWeightChoice = (weightsObj) => randomArraySelect(weightedSelectionList(weightsObj));

const generateRoutine = () => {

    // scaleWeights = weightedSelectionList(routineWeights["sequence routine"]["small jump"]["scale"]);

    for (let i = 0; i<1; i++) {
        console.log(randomWeightChoice(routineWeights["sequence routine"]["small jump"]["scale"]));
        console.log(randomWeightChoice(routineWeights["sequence routine"]["small jump"]["harmonic pattern"]));

        console.log(randomWeightChoice(routineWeights["sequence routine"]["big jump"]["scale"]));
        console.log(randomWeightChoice(routineWeights["sequence routine"]["big jump"]["harmonic pattern"]));

        console.log(randomWeightChoice(routineWeights["sequence routine"]["dynamic pattern"]["speed"]));
        console.log(randomWeightChoice(routineWeights["sequence routine"]["dynamic pattern"]["blocks"]));
        console.log(randomWeightChoice(routineWeights["sequence routine"]["dynamic pattern"]["dynamics"]));

        console.log(randomWeightChoice(routineWeights["sequence routine"]["articulation pattern"]));
        console.log(randomWeightChoice(routineWeights["sequence routine"]["articulation style"]));

        // console.log([...scaleWeights])
        // console.log(marbleRandomArraySelect(scaleWeights));
    }

    abcjs.renderAbc("paper", routineAbc);
}
