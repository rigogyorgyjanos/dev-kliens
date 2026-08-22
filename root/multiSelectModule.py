# Shared bulk-selection state for inventory / extended inventory item slots.
# Mirrors mouseModule.mouseController's role as a global singleton, so a
# selection started in one window (e.g. base inventory) can be dragged into
# another (extended inventory, shop, exchange) exactly like a normal
# single-item drag already can.

selectedSlotType = None
selectedSlots = []
dragSnapshot = []

def Clear():
	global selectedSlotType, selectedSlots
	selectedSlotType = None
	selectedSlots = []

def ToggleSlot(slotType, slotIndex):
	global selectedSlotType, selectedSlots

	if selectedSlotType != None and selectedSlotType != slotType:
		# Only one slotType can be selected at a time - a mixed-type bulk
		# move/drop/sell/trade wouldn't mean anything anyway.
		Clear()

	selectedSlotType = slotType

	key = (slotType, slotIndex)
	if key in selectedSlots:
		selectedSlots.remove(key)
		if not selectedSlots:
			selectedSlotType = None
	else:
		selectedSlots.append(key)

def IsSelected(slotType, slotIndex):
	return (slotType, slotIndex) in selectedSlots

def GetCount():
	return len(selectedSlots)

def GetSlots():
	return list(selectedSlots)

def BeginDrag(slotType, slotIndex):
	# Called right after the normal single-item pickup (AttachObject) already
	# ran, so the cursor visual never changes - we just remember, on the
	# side, that this particular drag actually represents the whole group.
	global dragSnapshot

	if GetCount() > 1 and IsSelected(slotType, slotIndex):
		dragSnapshot = GetSlots()
	else:
		dragSnapshot = []

def PopDragSnapshot():
	# Consumed exactly once by whichever bulk action (move/drop/sell/trade)
	# ends up handling the drop; always clears the whole selection afterward.
	global dragSnapshot

	snapshot = dragSnapshot
	dragSnapshot = []
	Clear()
	return snapshot
