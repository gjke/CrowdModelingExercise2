import os
import json

scenario_path = "C:\\Users\\Mehmet\\Desktop\\Test\\scenarios\\Corner.scenario"
scenario_output_path = "C:\\Users\\Mehmet\\Desktop\\Test\\scenarios\\CornerNew.scenario"
output_path = "C:\\Users\\Mehmet\\Desktop\\Test\\output"
vadere_path = 'D:\\Uni\\MS\\CoronaSemester3_Reloaded\\Praktikum\\Exercise2\\Vadere'
new_pedestrian_position = (12.0,2.0)

def create_new_pedestrian(position: (int,int), target:int):
    output = {}

    attributes = {}
    attributes['id'] = 1
    attributes['radius'] = 0.2
    attributes['densityDependentSpeed'] = False
    attributes['speedDistributionMean'] = 1.34
    attributes['speedDistributionStandardDeviation'] = 0.26
    attributes['minimumSpeed'] = 0.5
    attributes['maximumSpeed'] = 2.2
    attributes['acceleration'] = 2.0
    attributes['footstepHistorySize'] = 4
    attributes['searchRadius'] = 1.0
    attributes['walkingDirectionCalculation'] = 'BY_TARGET_CENTER'
    attributes['walkingDirectionSameIfAngleLessOrEqual'] = 45.0
    output['attributes'] = attributes

    output['source'] = None
    output['targetIds'] = [target]
    output['nextTargetListIndex'] = 0
    output['isCurrentTargetAnAgent'] = False
    output['position'] = {'x' : position[0], 'y': position[1]}
    output['velocity'] = {'x' : 0.0, 'y': 0.0}
    output['freeFlowSpeed'] = 1.1821257468417046
    output['followers'] = []
    output['idAsTarget'] = -1
    output['isChild'] = False
    output['isLikelyInjured'] = False

    psychology = {}
    psychology['mostImportantStimulus'] = None
    psychology['threatMemory'] = {'allThreats':[],'latestThreatUnhandled':False}
    psychology['selfCategory'] = 'TARGET_ORIENTED'
    psychology['groupMembership'] = 'OUT_GROUP'
    psychology['knowledgeBase'] = {'knowledge' : []}
    output['psychologyStatus'] = psychology

    output['groupIds'] = []
    output['trajectory'] = {'footSteps' : []}
    output['groupSizes'] = []
    output['modelPedestrianMap'] = {}
    output['type'] = 'PEDESTRIAN'

    return [output]

if __name__ == '__main__':
    #First open the scenario
    data = None
    with open(scenario_path) as json_file:
        data = json.load(json_file)
        #Next add the new pedestrian
        data['name'] = 'CornerNew' #Name of the new scenario
        data['scenario']['topography']['dynamicElements'] = create_new_pedestrian(new_pedestrian_position,data['scenario']['topography']['targets'][0]['id'])
        #Now write it back into the file

    with open(scenario_output_path,'w') as output:
        json.dump(data,output)
    #Now run the code
    os.chdir(vadere_path)
    os.system('java -jar vadere-console.jar scenario-run --scenario-file \"' + scenario_output_path + '\" --output-dir=\"' + output_path + '\"')