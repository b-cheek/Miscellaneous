var Formula = {
    _SlowVdotLimit: 39,

    getVDOT: function(distance, time) {
        var V = this._getVDOTSpeedParam(distance, time);
        var VO2 = this._getVO2(V);
        // fraction of VO2 max
        var F = .80 + .298956 * Math.exp(-.193261 * time) + .189439 * Math.exp(-.012778 * time);
        return VO2 / F;
    },

    _getVDOTSpeedParam(meters, minutes) {
        if (meters >= 1600) {
            return meters / minutes;
        }

        if (meters > 800) {
            const scale = 1600 / meters;
            const percentage = (1600 - meters) / 800;
            const adjustment = scale + 0.1 * percentage;
            const m1600Mins = minutes * adjustment;
            return 1600 / m1600Mins;
        } else {
            const m800Adjustment = 2.1;
            const distanceFactor = 800 / meters;
            const adjustment = distanceFactor * m800Adjustment;
            const m1600Mins = minutes * adjustment;
            return 1600 / m1600Mins;
        }
    },

    getPredictedRaceTime: function(VDOT, distance) {
        var A = distance / (4 * VDOT);
        for (var i = 0; i < 3; i++) {
            var B = Math.exp(-.193261 * A);
            var C = .298956 * B + Math.exp(-.012778 * A) * .189439 + .8;
            var E = Math.pow((VDOT * C), 2) * -.0075 + (VDOT * C) * 5.000663 + 29.54;
            var G = (.298956 * B) * .19326;
            var H = G - Math.exp(-.012778 * A) * .189439 * (-.012778);
            var I = (C * H * VDOT) * (-.007546) * 3;
            var J = (H * VDOT) * 5.000663 + I;
            var K = (distance * J) / Math.pow(E, 2) + 1;
            var L = A - (distance / E);
            var P = L / K;
            A = A - P;
        }
        const V = distance / A;
        const time = distance / V; // distance over velocity

        if (distance >= 1600) {
            return time;
        }

        const adjustedV = this._getVDOTSpeedParam(distance, time);

        const scale = V / adjustedV;
        return time / scale;
    },

    getMarathonPace: function(VDOT, trainingDistance) {
        return trainingDistance / Formula._getMarathonVelocity(VDOT);
    },

    getJogPace: function(vdot, distance) {
        if (vdot > 50.5) {
            const pace = 9.0 * Conversion.toMiles(distance);
            return pace;
        }

        return this.getEasyPace(vdot, distance, true);
    },

    getWalkPace: function(distance) {
        const pace = 12 * (1000 / distance);
        return pace;
    },

    getEasyPace: function(vdot, distance, slowerPace) {
        if (this._isSlowVdot(vdot)) {
            vdot = this._getSRVDOT(vdot);
        }

        var percentage = slowerPace ? .62 : .70;
        return this._getCustomEffortPace(vdot, distance, percentage);
    },

    getEasyPaceRange: function(vdot, distance, unit) {
        const slower = this.getEasyPace(vdot, distance, true);
        const faster = this.getEasyPace(vdot, distance, false);

        return {
            slow: slower,
            fast: faster,
            unit: unit
        };
    },
    
    getThresholdPace: function(vdot, distance) {
        if (this._isSlowVdot(vdot)) {
            var srvdot = this._getSRVDOT(vdot);
            vdot = (srvdot + parseFloat(vdot)) / 2;
        }

        return this._getCustomEffortPace(vdot, distance, .88);
    },

    getIntervalPace: function(vdot, distance) {
        if (this._isSlowVdot(vdot)) {
            vdot = this._getSRVDOT(vdot);
        }

        return this._getCustomEffortPace(vdot, distance, .975);
    },

    getRepetitionPace: function(vdot, distance) {
        const per400FasterBy = 6.0;
        const divisor = (distance / 400) * (per400FasterBy / 60);

        const pace = this.getIntervalPace(vdot, distance);
        return pace - divisor;
    },

    
    getFastRepsPace: function(vdot, distance) {
        var per200FasterBy = 4.0;
        var divisor = (distance / 200) * (per200FasterBy / 60);

        // 200m - 4s
        // 1000m - 20s
//        if (distance === 200) {
//            toSubtract = 4 / 60;
//        } else if (distance === 300) {
//            toSubtract = 6 / 60;
//        } else if (distance === 400) {
//            toSubtract = 8 / 60;
//        } else if (distance === 600) {
//            toSubtract = 12 / 60;
//        } 

        var pace = this.getRepetitionPace(vdot, distance);
        return pace - divisor;
    },

    isFastRepsDistance: function(distance) {
        return distance === 200 ||
            distance === 300 ||
            distance === 400 ||
            distance === 600;
    },

    getCustomTrainingPace: function(paceType, percentage, distanceMeters, vdot, paceUnit) {
        if (paceType === CustomTrainingPaceType.Effort) {
            if (this._isSlowVdot(vdot)) {
                vdot = this._getSRVDOT(vdot);
            }

            const paceDistance = FormulaHelpers.getPaceDistanceForUnit(paceUnit);
            return this._getCustomEffortPace(vdot, paceDistance, percentage / 100);
        }
        
        return this._getCustomDistancePace(vdot, distanceMeters, paceUnit);
    },

    _isSlowVdot: function(vdot) {
        return vdot > 0 && vdot < Formula._SlowVdotLimit;
    },

    _getSRVDOT: function(vdot) {
        return (vdot * 2 / 3) + 13;
    },

    _getCustomEffortPace: function(vdot, distance, percentage) {
        var O = vdot * percentage;
        var V = Formula._getPaceVelocity(O);
        return distance / V;
    },

    _getCustomDistancePace: function(vdot, meters, paceUnit) {
        const raceTime = this.getPredictedRaceTime(vdot, meters);
        const paceDistance = FormulaHelpers.getPaceDistanceForUnit(paceUnit);
        const distanceInPaceUnit = meters / paceDistance;

        return raceTime / distanceInPaceUnit;
    },

    _getVO2: function(V) {
        return .182258 * V + .000104 * Math.pow(V, 2) - 4.6;
    },

    _getPaceVelocity: function(O) {
        return 29.54 + 5.000663 * O - .007546 * Math.pow(O, 2);
    },

    _getMarathonVelocity: function(VDOT) {
        var distance = 42195;
        var A = distance / (4 * VDOT);
        for (var i = 0; i < 3; i++) {
            var B = Math.exp(-.193261 * A);
            var C = .298956 * B + Math.exp(-.012778 * A) * .189439 + .8;
            var E = Math.pow((VDOT * C), 2) * -.0075 + (VDOT * C) * 5.000663 + 29.54;
            var G = (.298956 * B) * .19326;
            var H = G - Math.exp(-.012778 * A) * .189439 * (-.012778);
            var I = (C * H * VDOT) * (-.007546) * 3;
            var J = (H * VDOT) * 5.000663 + I;
            var K = (distance * J) / Math.pow(E, 2) + 1;
            var L = A - (distance / E);
            var P = L / K;
            A = A - P;
        }
        return distance / A;
        /*var V = distance / A;
        return trainingDistance / V;*/
    }

};

var FormulaHelpers = {
    getPaceUnitForUser: function(unit, user) {
        var unitEnum = DistanceUnit.enumValue(unit);
        return Conversion.isPaceUnit(unitEnum) ? unitEnum : user.mikm;
    },

    getPaceDistanceForUnit: function(paceUnit) {
        var unitEnum = DistanceUnit.enumValue(paceUnit);
        return unitEnum === DistanceUnit.mi ? Conversion.fromMiles(1) : 1000;
    },

    getEasyPaceRangeForUnit: function(vdot, paceUnit) {
        const distance = this.getPaceDistanceForUnit(paceUnit);
        return Formula.getEasyPaceRange(vdot, distance, paceUnit);
    },

    getQualitySetItemPaces: function(user, distance, distanceUnit, effort, customPace) {
        const sessionType = QualitySessionType.enumValue(effort);

        distanceUnit = DistanceUnit.enumValue(distanceUnit);
        const userPreferredUnit = DistanceUnit.enumValue(user.mikm);
        const isRepetition = this._isRepetitionSet(distanceUnit, userPreferredUnit);
        
        // Note: For repetitions, we use default user unit to calculate pace
        const paceUnit = isRepetition ? userPreferredUnit : this.getPaceUnitForUser(distanceUnit, user);
        const paceDistance = this.getPaceDistanceForUnit(paceUnit);

        // Note: For time set items we just use the same calculations as for mi/km paces
        const repDistance = Conversion.isTimeUnit(distanceUnit) ? paceDistance : Conversion.fromDistanceUnitString(distance, distanceUnit, true, false);
        
        var pace = 0;
        var repTime = 0;

        if (customPace != null) {
            pace = Formula.getCustomTrainingPace(customPace.paceType, customPace.percentage, customPace.distanceMeters, user.VDOT, paceUnit);
        } else if (sessionType === QualitySessionType.FastReps) {

            // Note: here we need to update pace on the repTime, which is why we invert the and calculate pace from repTime
            repTime = Formula.getFastRepsPace(user.VDOT, repDistance);
            pace = this.getQualitySetRepPace(repTime, repDistance, paceUnit);
        } else {
            pace = FormulaHelpers.getQualitySessionPace(sessionType, user.VDOT, paceDistance);
        }

        if (pace && pace > 0 && repTime === 0) {
            repTime = this.getQualitySetRepTime(pace, paceUnit, repDistance);
        }

        return {
            pace: pace,
            repTime: repTime,
            paceUnit: paceUnit,
            isRepetition: isRepetition
        };
    },

    getQualitySessionPace: function(sessionType, vdot, distance) {
        switch (sessionType) {
        case QualitySessionType.Easy:
            return Formula.getEasyPace(vdot, distance);
        case QualitySessionType.Threshold:
            return Formula.getThresholdPace(vdot, distance);
        case QualitySessionType.Interval:
            return Formula.getIntervalPace(vdot, distance);
        case QualitySessionType.Repetition:
            return Formula.getRepetitionPace(vdot, distance);
        case QualitySessionType.FastReps:
            return Formula.getFastRepsPace(vdot, distance);
        case QualitySessionType.Marathon:
            return Formula.getMarathonPace(vdot, distance);
            break;
        case QualitySessionType.Hills: // We don't show paces for hills
            return Formula.getIntervalPace(vdot, distance);
        default:
            return 0;
        }
    },

    getPaceRangeForWorkoutSet: function(user, pace, distanceUnit, sessionType) {
        if (sessionType === QualitySessionType.Hills) {
            return { slow: 0, fast: 0, unit: distanceUnit }
        } else if (sessionType === QualitySessionType.Easy) {
            const paceUnit = this.getPaceUnitForUser(distanceUnit, user);
            const slowPace = this.getSlowPaceForEasyWorkoutSet(user, pace, paceUnit);
            return { slow: slowPace, fast: pace, unit: paceUnit }
        } else {
            const isRepUnit = distanceUnit === DistanceUnit.rep || distanceUnit === DistanceUnit.meter;
            const paceUnit = isRepUnit ? DistanceUnit.rep : this.getPaceUnitForUser(distanceUnit, user);

            return { slow: 0, fast: pace, unit: paceUnit }
        }
    },

    getSlowPaceForEasyWorkoutSet: function(user, pace, paceUnit) {
        const paceDistance = this.getPaceDistanceForUnit(paceUnit);
        const easyRange = Formula.getEasyPaceRange(user.VDOT, paceDistance, paceUnit);

        const diff = easyRange.fast - pace;
        if (easyRange.slow < pace || diff / pace > 0.1) {
            return pace + 0.3333;
        }

        return easyRange.slow;
    },

    getQualitySetRepTime: function(pace, paceUnit, repDistance) {
        var paceDistance = this.getPaceDistanceForUnit(paceUnit);
        var repTime = pace * repDistance / paceDistance;
        
        return repTime;
    },

    getQualitySetRepPace: function(repTime, repDistanceMeters, paceUnit) {
        // var fullSeconds = Conversion.roundToFullSeconds(repTime);
        var paceDistance = this.getPaceDistanceForUnit(paceUnit);
        var pace = paceDistance * repTime / repDistanceMeters;

        return pace;
    },

    getQualityWorkoutRecoveryMeters: function(repsCount, recoveryAmount, recoveryUnit, vdot) {
        var recoveryMeters = this.getQualityWorkoutSingleRecoveryMeters(repsCount, recoveryAmount, recoveryUnit, vdot);

        return (repsCount - 1) * recoveryMeters;
    },

    getQualityWorkoutSingleRecoveryMeters: function(repsCount, recoveryAmount, recoveryUnit, vdot) {
        if (repsCount <= 1 || recoveryAmount <= 0) {
            return 0;
        }

        var recoveryDistanceUnit = Conversion.recoveryToDistanceUnit(recoveryUnit);

        if (Conversion.isTimeUnit(recoveryDistanceUnit)) {
            return Conversion.getRecoveryDistanceFromTime(recoveryAmount, recoveryUnit, vdot);
        } else {
            return Conversion.toMetersFromUnits(recoveryAmount, recoveryDistanceUnit);
        }
    },
    
    isWorkoutSet: function(sessionType) {
        var value = QualitySessionType.enumValue(sessionType);

        return value !== QualitySessionType.Rest && value !== QualitySessionType.Text;
    },

    isRaceTimeEquivalentToVdot: function(time, distance, vdot) {
        if (time === 0 && distance === 0) {
            return true;
        } else if (distance === 0) {
            return false;
        }

        var vdotEquivalentTime = Formula.getPredictedRaceTime(vdot, distance);
        var timeText = Formatting.toMinutes(time);
        var vdotEquivalentText = Formatting.toMinutes(vdotEquivalentTime);
        return timeText === vdotEquivalentText;
    },

    _isRepetitionSet: function(distanceUnit, userPreferredUnit) {
        if (Conversion.isTimeUnit(distanceUnit)) {
            return false;
        }

        return distanceUnit === DistanceUnit.m ||
            distanceUnit === DistanceUnit.rep ||
            userPreferredUnit !== distanceUnit;
    },

    getMiPace: function(distance, totalTime) {
        const paceTotalDistance = Conversion.toMiles(distance);
        return totalTime / paceTotalDistance;
    },

    getKmPace(distance, totalTime) {
        const paceTotalDistance = Conversion.toKilometers(distance);
        return totalTime / paceTotalDistance;
    },
}

var distance = 1600;
var minutes = 5;
var vdot = Formula.getVDOT(distance, minutes);