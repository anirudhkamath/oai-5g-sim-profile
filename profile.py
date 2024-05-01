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

NUC_HARDWARES = ("nuc1", "nuc2")
# NUC_HWTYPE = "nuc5300"
BIN_PATH = "/local/repository/bin"
DEPLOY_OAI_UE = os.path.join(BIN_PATH, "start-oai-ue.sh")
DEPLOY_OAI_GNB = os.path.join(BIN_PATH, "start-oai.sh")
DEPLOY_INTERFERER = os.path.join(BIN_PATH, "start-awgn-interferer.sh")

pc = portal.Context()

nuc_to_hw_type = {
    "nuc1": "nuc5300",
    "nuc2": "nuc5300"
}

pc.defineParameter(
    "gnb1_node",
    "Node for gnb",
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
ue.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"  # for now just deploy the same disk image.
ue.Desire("rf-controlled", 1)
ue_gnb1_rf = ue.addInterface("ue_gnb1_rf")
ue.addService(rspec.Execute(shell="bash", command="/local/repository/bin/deploy-oai.sh develop ue"))
ue.startVNC()
# ue.addService(rspec.Execute(shell="bash"))

gnb1 = request.RawPC("gnb1")
gnb1.component_id = params.gnb1_node
gnb1.hardware_type = nuc_to_hw_type[params.gnb1_node]
gnb1.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"
gnb1.Desire("rf-controlled", 1)
gnb1_ue_rf = gnb1.addInterface("gnb1_ue_rf")
gnb1_core_node_intf = gnb1.addInterface("gnb1_core_interface")
gnb1_core_node_intf.addAddress(rspec.IPv4Address("192.168.1.20", "255.255.255.0"))  # gNB endpoint for core link.
gnb1.addService(rspec.Execute(shell="bash", command="/local/repository/bin/deploy-oai.sh develop nodeb"))
gnb1.startVNC()
# gnb1.addService(rspec.Execute(shell="bash"))


# core node.
core_node = request.RawPC( "core" )
core_node.hardware_type = "d430"
core_node.disk_image = "urn:publicid:IDN+emulab.net+image+emulab-ops//UBUNTU22-64-STD"
core_node_gnb_intf = core_node.addInterface("core_gnb1_interface")
core_node_gnb_intf.addAddress(rspec.IPv4Address("192.168.1.10", "255.255.255.0"))  # NGAP (AMF, UP)
core_node.addService(rspec.Execute(shell="bash", command="/local/repository/bin/deploy-open5gs.sh"))
core_node.startVNC()

# interferer = request.RawPC("interferer")
# interferer.hardware_type = NUC_HWTYPE
# interferer.component_id = params.interferer_node
# interferer.disk_image = "urn:publicid:IDN+emulab.net+image+TimeTravel5G:oai-5g-sim-with-bbr"
# # gnb1_s1_if = gnb1.addInterface("gnb1_s1_if")
# # gnb1_s1_if.addAddress(rspec.IPv4Address("192.168.1.2", "255.255.255.0"))
# interferer.Desire("rf-controlled", 1)
# interferer_ue_rf = interferer.addInterface("interferer_ue_rf")
# interferer.addService(rspec.Execute(shell="bash", command=DEPLOY_INTERFERER))
# # gnb1.addService(rspec.Execute(shell="bash", command=TUNE_CPU))

# Create RF links between the UE and eNodeBs
rflink1 = request.RFLink("rflink1")
rflink1.addInterface(gnb1_ue_rf)
rflink1.addInterface(ue_gnb1_rf)
cn_link = request.Link("cn-link")
cn_link.setNoBandwidthShaping()
cn_link.addInterface(core_node_gnb_intf)
cn_link.addInterface(gnb1_core_node_intf)
# rflink2 = request.RFLink("rflink2")
# rflink2.addInterface(interferer_ue_rf)
# rflink2.addInterface(ue_interferer_rf)

tour = IG.Tour()
tour.Description(IG.Tour.MARKDOWN, tourDescription)
tour.Instructions(IG.Tour.MARKDOWN, tourInstructions)
request.addTour(tour)

portal.context.printRequestRSpec()
