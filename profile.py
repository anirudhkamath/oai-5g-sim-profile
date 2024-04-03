#!/usr/bin/python

tourDescription = """
### Running TCP experiments over 5G OpenAirInterface5G controlled RF experiments on POWDER

This profile is derived from a tutorial session created by Dustin Maas for MERIF 2023.
It deploys one gNB, one interference, and one UE compute nodes with an image that includes docker,
docker-compose, tshark, oai-cn5g-fed v1.4.0, and docker images for all of the
OAI 5G core network functions. It also includes source code and a prebuilt
version of the OAI RAN stack (gNB, nrUE, RF simulator).

The description and instructions for the original MERIF session can be found
[here](https://gitlab.flux.utah.edu/powderrenewpublic/merif2023/-/blob/main/content/teaching-5g-oai.md).
"""

tourInstructions = """

Note: After you instantiate an experiment, you have to wait until the POWDER
portal shows your experiment status in green as "Your experiment is ready"
before proceeding.


"""

import os

import geni.portal as portal
import geni.rspec.pg as rspec
import geni.urn as URN
import geni.rspec.igext as IG
import geni.rspec.emulab.pnext as PN
import geni.rspec.emulab as emulab

NUC_HARDWARES = ("nuc27", "nuc23")
# NUC_HWTYPE = "nuc5300"
BIN_PATH = "/local/repository/bin"
DEPLOY_OAI_UE = os.path.join(BIN_PATH, "start-oai-ue.sh")
DEPLOY_OAI_GNB = os.path.join(BIN_PATH, "start-oai.sh")
DEPLOY_INTERFERER = os.path.join(BIN_PATH, "start-awgn-interferer.sh")

pc = portal.Context()

nuc_to_hw_type = {
    "nuc27": "nuc8259",
    "nuc23": "nuc8650"
}

pc.defineParameter(
    "enb1_node",
    "Node for eNB",
    portal.ParameterType.STRING,
    NUC_HARDWARES[0],
    NUC_HARDWARES
)

pc.defineParameter(
    "ue_node",
    "Node for UE",
    portal.ParameterType.STRING,
    NUC_HARDWARES[1],
    NUC_HARDWARES
)

params = pc.bindParameters()
pc.verifyParameters()
request = pc.makeRequestRSpec()

ue = request.RawPC("ue")
ue.component_id = params.ue_node
ue.hardware_type = nuc_to_hw_type[params.ue_node]
ue.disk_image = "urn:publicid:IDN+emulab.net+image+TimeTravel5G:oai-5g-sim-with-bbr"  # for now just deploy the same disk image.
ue_enb1_rf = ue.addInterface("ue_enb1_rf")
# ue_interferer_rf = ue.addInterface("ue_interferer_rf")
ue.addService(rspec.Execute(shell="bash", command=DEPLOY_OAI_UE))

enb1 = request.RawPC("enb1")
enb1.component_id = params.enb1_node
enb1.hardware_type = nuc_to_hw_type[params.enb1]
enb1.disk_image = "urn:publicid:IDN+emulab.net+image+TimeTravel5G:oai-5g-sim-with-bbr"
# enb1_s1_if = enb1.addInterface("enb1_s1_if")
# enb1_s1_if.addAddress(rspec.IPv4Address("192.168.1.2", "255.255.255.0"))
enb1.Desire("rf-controlled", 1)
enb1_ue_rf = enb1.addInterface("enb1_ue_rf")
enb1.addService(rspec.Execute(shell="bash", command=DEPLOY_OAI_GNB))
# enb1.addService(rspec.Execute(shell="bash", command=TUNE_CPU))

# interferer = request.RawPC("interferer")
# interferer.hardware_type = NUC_HWTYPE
# interferer.component_id = params.interferer_node
# interferer.disk_image = "urn:publicid:IDN+emulab.net+image+TimeTravel5G:oai-5g-sim-with-bbr"
# # enb1_s1_if = enb1.addInterface("enb1_s1_if")
# # enb1_s1_if.addAddress(rspec.IPv4Address("192.168.1.2", "255.255.255.0"))
# interferer.Desire("rf-controlled", 1)
# interferer_ue_rf = interferer.addInterface("interferer_ue_rf")
# interferer.addService(rspec.Execute(shell="bash", command=DEPLOY_INTERFERER))
# # enb1.addService(rspec.Execute(shell="bash", command=TUNE_CPU))

# Create RF links between the UE and eNodeBs
rflink1 = request.RFLink("rflink1")
rflink1.addInterface(enb1_ue_rf)
rflink1.addInterface(ue_enb1_rf)
# rflink2 = request.RFLink("rflink2")
# rflink2.addInterface(interferer_ue_rf)
# rflink2.addInterface(ue_interferer_rf)

# node = request.RawPC( "node" )
# node.hardware_type = "d430"
# node.disk_image = "urn:publicid:IDN+emulab.net+image+TimeTravel5G:oai-5g-sim-with-bbr"  # disk image on POWDER.
# node.startVNC()

tour = IG.Tour()
tour.Description(IG.Tour.MARKDOWN, tourDescription)
tour.Instructions(IG.Tour.MARKDOWN, tourInstructions)
request.addTour(tour)

portal.context.printRequestRSpec()
