.. _telemetry-specification:

======================================
F1 2020 Telemetry Packet Specification
======================================

.. note::

   This specification was copied (with the minor changes listed below) from the CodeMasters forum topic describing the F1 2020 telemetry UDP packet specification, as found here:

     https://forums.codemasters.com/topic/54423-f1%C2%AE-2020-udp-specification/

   The forum post has one post detailing packet formats, followed by a post with Frequently Asked Questions, followed by a post with appendices, giving a number of lookup tables.
   The package format and appendices have been reproduced here; for the FAQ, please refer to the original forum topic.

   The following changes were made in the process of copying the specification:

   * Added suffix '\_t' to all integer types, bringing the type names in lines with the types declared in the standard C header file ``<stdint.h>`` (equivalent to ``<cstdint>`` in C++). This change also improves the syntax highlighting of the struct definitions below.
   * Added the *uint32_t* type to the *Packet Types* table;
   * In struct *PacketMotionData*: corrected comments of the fields *m_angularAccelerationX*, *m_angularAccelerationY*,
     and *m_angularAccelerationZ* to reflect that the values represent accelerations rather than velocities;
   * In struct *CarSetupData*: corrected comment of field *m_rearAntiRollBar* to refer to *rear* instead of *front*;
   * In the Driver IDs appendix: corrected the name of driver 34: *Wilheim Kaufmann* to *Wilhelm Kaufmann*.

The F1 series of games support the output of certain game data across UDP connections.
This data can be used supply race information to external applications, or to drive certain hardware (e.g. motion platforms, force feedback steering wheels and LED devices).

The following information summarise this data structures so that developers of supporting hardware or software are able to configure these to work correctly with the F1 game.

If you cannot find the information that you require then please contact community@codemasters.com and a member of the dev team will respond to your query as soon as possible.

------------------
Packet Information
------------------

.. note::

   The structure definitions given below are specified in the syntax of the C programming language.

   The Python versions of the structures provided by the *f1-telemetry-packet* package are very similar to the C versions, with the notable exception that for all field names, the 'm\_' prefix is omitted. For example, the header field *m_packetFormat* is just called *packetFormat* in the Python version.

^^^^^^^^^^^^
Packet Types
^^^^^^^^^^^^

Each packet can now carry different types of data rather than having one packet which contains everything.
A header has been added to each packet as well so that versioning can be tracked and it will be easier for applications to check they are interpreting the incoming data in the correct way.
Please note that all values are encoded using Little Endian format.
All data is packed.

The following data types are used in the structures:

+----------+-------------------------+
| Type     | Description             |
+==========+=========================+
| uint8_t  | Unsigned 8-bit integer  |
+----------+-------------------------+
| int8_t   | Signed 8-bit integer    |
+----------+-------------------------+
| uint16_t | Unsigned 16-bit integer |
+----------+-------------------------+
| int16_t  | Signed 16-bit integer   |
+----------+-------------------------+
| uint32_t | Unsigned 32-bit integer |
+----------+-------------------------+
| float    | Floating point (32-bit) |
+----------+-------------------------+
| uint64_t | Unsigned 64-bit integer |
+----------+-------------------------+

^^^^^^^^^^^^^
Packet Header
^^^^^^^^^^^^^

Each packet has the following header:

.. code-block:: c

   struct PacketHeader
   {
       uint16_t  m_packetFormat;            // 2020
       uint8_t   m_gameMajorVersion;        // Game major version - "X.00"
       uint8_t   m_gameMinorVersion;        // Game minor version - "1.XX"
       uint8_t   m_packetVersion;           // Version of this packet type, all start from 1
       uint8_t   m_packetId;                // Identifier for the packet type, see below
       uint64_t  m_sessionUID;              // Unique identifier for the session
       float     m_sessionTime;             // Session timestamp
       uint32_t  m_frameIdentifier;         // Identifier for the frame the data was retrieved on
       uint8_t   m_playerCarIndex;          // Index of player's car in the array
       uint8_t   m_secondaryPlayerCarIndex; // Index of secondary player's car in the array (splitscreen)
                                            // 255 if no second player
   };

""""""""""
Packet IDs
""""""""""

The packets IDs are as follows:

+---------------+-------+----------------------------------------------------------------------------------+
| Packet Name   | Value | Description                                                                      |
+===============+=======+==================================================================================+
| Motion        | 0     | Contains all motion data for player's car – only sent while player is in control |
+---------------+-------+----------------------------------------------------------------------------------+
| Session       | 1     | Data about the session – track, time left                                        |
+---------------+-------+----------------------------------------------------------------------------------+
| Lap Data      | 2     | Data about all the lap times of cars in the session                              |
+---------------+-------+----------------------------------------------------------------------------------+
| Event         | 3     | Various notable events that happen during a session                              |
+---------------+-------+----------------------------------------------------------------------------------+
| Participants  | 4     | List of participants in the session, mostly relevant for multiplayer             |
+---------------+-------+----------------------------------------------------------------------------------+
| Car Setups    | 5     | Packet detailing car setups for cars in the race                                 |
+---------------+-------+----------------------------------------------------------------------------------+
| Car Telemetry | 6     | Telemetry data for all cars                                                      |
+---------------+-------+----------------------------------------------------------------------------------+
| Car Status    | 7     | Status data for all cars such as damage                                          |
+---------------+-------+----------------------------------------------------------------------------------+
| Final         | 8     | Final classification confirmation at the end of a race                           |
| Classification|       |                                                                                  |
+---------------+-------+----------------------------------------------------------------------------------+
| Lobby Info    | 9     | Information about players in a multiplayer lobby                                 |
+---------------+-------+----------------------------------------------------------------------------------+

^^^^^^^^^^^^^
Motion Packet
^^^^^^^^^^^^^

The motion packet gives physics data for all the cars being driven. There is additional data for the car being driven with the goal of being able to drive a motion platform setup.

*N.B. For the normalised vectors below, to convert to float values divide by 32767.0f – 16-bit signed values are used to pack the data and on the assumption that direction values are always between -1.0f and 1.0f.*

| Frequency: Rate as specified in menus
| Size: 1464 bytes
| Version: 1

.. code-block:: c

   struct CarMotionData
   {
       float         m_worldPositionX;           // World space X position
       float         m_worldPositionY;           // World space Y position
       float         m_worldPositionZ;           // World space Z position
       float         m_worldVelocityX;           // Velocity in world space X
       float         m_worldVelocityY;           // Velocity in world space Y
       float         m_worldVelocityZ;           // Velocity in world space Z
       int16_t       m_worldForwardDirX;         // World space forward X direction (normalised)
       int16_t       m_worldForwardDirY;         // World space forward Y direction (normalised)
       int16_t       m_worldForwardDirZ;         // World space forward Z direction (normalised)
       int16_t       m_worldRightDirX;           // World space right X direction (normalised)
       int16_t       m_worldRightDirY;           // World space right Y direction (normalised)
       int16_t       m_worldRightDirZ;           // World space right Z direction (normalised)
       float         m_gForceLateral;            // Lateral G-Force component
       float         m_gForceLongitudinal;       // Longitudinal G-Force component
       float         m_gForceVertical;           // Vertical G-Force component
       float         m_yaw;                      // Yaw angle in radians
       float         m_pitch;                    // Pitch angle in radians
       float         m_roll;                     // Roll angle in radians
   };

   struct PacketMotionData
   {
       PacketHeader    m_header;                // Header

       CarMotionData   m_carMotionData[22];     // Data for all cars on track

       // Extra player car ONLY data
       float         m_suspensionPosition[4];       // Note: All wheel arrays have the following order:
       float         m_suspensionVelocity[4];       // RL, RR, FL, FR
       float         m_suspensionAcceleration[4];   // RL, RR, FL, FR
       float         m_wheelSpeed[4];               // Speed of each wheel
       float         m_wheelSlip[4];                // Slip ratio for each wheel
       float         m_localVelocityX;              // Velocity in local space
       float         m_localVelocityY;              // Velocity in local space
       float         m_localVelocityZ;              // Velocity in local space
       float         m_angularVelocityX;            // Angular velocity x-component
       float         m_angularVelocityY;            // Angular velocity y-component
       float         m_angularVelocityZ;            // Angular velocity z-component
       float         m_angularAccelerationX;        // Angular acceleration x-component
       float         m_angularAccelerationY;        // Angular acceleration y-component
       float         m_angularAccelerationZ;        // Angular acceleration z-component
       float         m_frontWheelsAngle;            // Current front wheels angle in radians
   };

^^^^^^^^^^^^^^
Session Packet
^^^^^^^^^^^^^^

The session packet includes details about the current session in progress.

| Frequency: 2 per second
| Size: 251 bytes
| Version: 1

.. code-block:: c

   struct MarshalZone
   {
       float  m_zoneStart;   // Fraction (0..1) of way through the lap the marshal zone starts
       int8_t m_zoneFlag;    // -1 = invalid/unknown, 0 = none, 1 = green, 2 = blue, 3 = yellow, 4 = red
   };

   struct WeatherForecastSample
   {
       uint8_t   m_sessionType;                     // 0 = unknown, 1 = P1, 2 = P2, 3 = P3, 4 = Short P, 5 = Q1
                                                    // 6 = Q2, 7 = Q3, 8 = Short Q, 9 = OSQ, 10 = R, 11 = R2
                                                    // 12 = Time Trial
       uint8_t   m_timeOffset;                      // Time in minutes the forecast is for
       uint8_t   m_weather;                         // Weather - 0 = clear, 1 = light cloud, 2 = overcast
                                                    // 3 = light rain, 4 = heavy rain, 5 = storm
       int8_t    m_trackTemperature;                // Track temp. in degrees celsius
       int8_t    m_airTemperature;                  // Air temp. in degrees celsius
   };

   struct PacketSessionData
   {
       PacketHeader    m_header;                    // Header

       uint8_t         m_weather;                   // Weather - 0 = clear, 1 = light cloud, 2 = overcast
                                                    // 3 = light rain, 4 = heavy rain, 5 = storm
       int8_t          m_trackTemperature;          // Track temp. in degrees celsius
       int8_t          m_airTemperature;            // Air temp. in degrees celsius
       uint8_t         m_totalLaps;                 // Total number of laps in this race
       uint16_t        m_trackLength;               // Track length in metres
       uint8_t         m_sessionType;               // 0 = unknown, 1 = P1, 2 = P2, 3 = P3, 4 = Short P
                                                    // 5 = Q1, 6 = Q2, 7 = Q3, 8 = Short Q, 9 = OSQ
                                                    // 10 = R, 11 = R2, 12 = Time Trial
       int8_t          m_trackId;                   // -1 for unknown, 0-21 for tracks, see appendix
       uint8_t         m_formula;                   // Formula, 0 = F1 Modern, 1 = F1 Classic, 2 = F2,
                                                    // 3 = F1 Generic
       uint16_t        m_sessionTimeLeft;           // Time left in session in seconds
       uint16_t        m_sessionDuration;           // Session duration in seconds
       uint8_t         m_pitSpeedLimit;             // Pit speed limit in kilometres per hour
       uint8_t         m_gamePaused;                // Whether the game is paused
       uint8_t         m_isSpectating;              // Whether the player is spectating
       uint8_t         m_spectatorCarIndex;         // Index of the car being spectated
       uint8_t         m_sliProNativeSupport;       // SLI Pro support, 0 = inactive, 1 = active
       uint8_t         m_numMarshalZones;           // Number of marshal zones to follow
       MarshalZone     m_marshalZones[21];          // List of marshal zones – max 21
       uint8_t         m_safetyCarStatus;           // 0 = no safety car, 1 = full safety car
                                                    // 2 = virtual safety car
       uint8_t         m_networkGame;               // 0 = offline, 1 = online
       uint8_t         m_numWeatherForecastSamples; // Number of weather samples to follow
       WeatherForecastSample m_weatherForecastSamples[20]; // Array of weather forecast samples
   };

^^^^^^^^^^^^^^^
Lap Data Packet
^^^^^^^^^^^^^^^

The lap data packet gives details of all the cars in the session.

| Frequency: Rate as specified in menus
| Size: 1190 bytes
| Version: 1

.. code-block:: c

   struct LapData
   {
       float       m_lastLapTime;               // Last lap time in seconds
       float       m_currentLapTime;            // Current time around the lap in seconds
       uint16_t    m_sector1TimeInMS;           // Sector 1 time in milliseconds
       uint16_t    m_sector2TimeInMS;           // Sector 2 time in milliseconds
       float       m_bestLapTime;               // Best lap time of the session in seconds
       uint8_t     m_bestLapNum;                // Lap number best time achieved on
       uint16_t    m_bestLapSector1TimeInMS;    // Sector 1 time of best lap in the session in milliseconds
       uint16_t    m_bestLapSector2TimeInMS;    // Sector 2 time of best lap in the session in milliseconds
       uint16_t    m_bestLapSector3TimeInMS;    // Sector 3 time of best lap in the session in milliseconds
       uint16_t    m_bestOverallSector1TimeInMS;// Best overall sector 1 time of the session in milliseconds
       uint8_t     m_bestOverallSector1LapNum;  // Lap number best overall sector 1 time achieved on
       uint16_t    m_bestOverallSector2TimeInMS;// Best overall sector 2 time of the session in milliseconds
       uint8_t     m_bestOverallSector2LapNum;  // Lap number best overall sector 2 time achieved on
       uint16_t    m_bestOverallSector3TimeInMS;// Best overall sector 3 time of the session in milliseconds
       uint8_t     m_bestOverallSector3LapNum;  // Lap number best overall sector 3 time achieved on
       float       m_lapDistance;               // Distance vehicle is around current lap in metres – could
                                                // be negative if line hasn’t been crossed yet
       float       m_totalDistance;             // Total distance travelled in session in metres – could
                                                // be negative if line hasn’t been crossed yet
       float       m_safetyCarDelta;            // Delta in seconds for safety car
       uint8_t     m_carPosition;               // Car race position
       uint8_t     m_currentLapNum;             // Current lap number
       uint8_t     m_pitStatus;                 // 0 = none, 1 = pitting, 2 = in pit area
       uint8_t     m_sector;                    // 0 = sector1, 1 = sector2, 2 = sector3
       uint8_t     m_currentLapInvalid;         // Current lap invalid - 0 = valid, 1 = invalid
       uint8_t     m_penalties;                 // Accumulated time penalties in seconds to be added
       uint8_t     m_gridPosition;              // Grid position the vehicle started the race in
       uint8_t     m_driverStatus;              // Status of driver - 0 = in garage, 1 = flying lap
                                                // 2 = in lap, 3 = out lap, 4 = on track
       uint8_t     m_resultStatus;              // Result status - 0 = invalid, 1 = inactive, 2 = active
                                                // 3 = finished, 4 = disqualified, 5 = not classified
                                                // 6 = retired
   };

   struct PacketLapData
   {
       PacketHeader    m_header;              // Header

       LapData         m_lapData[22];         // Lap data for all cars on track
   };

^^^^^^^^^^^^
Event Packet
^^^^^^^^^^^^

This packet gives details of events that happen during the course of a session.

| Frequency: When the event occurs
| Size: 35 bytes
| Version: 1

.. code-block:: c

   // The event details packet is different for each type of event.
   // Make sure only the correct type is interpreted.

   union EventDataDetails
   {
       struct
       {
           uint8_t      vehicleIdx; // Vehicle index of car achieving fastest lap
           float        lapTime;    // Lap time is in seconds
       } FastestLap;

       struct
       {
           uint8_t vehicleIdx; // Vehicle index of car retiring
       } Retirement;

       struct
       {
           uint8_t vehicleIdx; // Vehicle index of team mate
       } TeamMateInPits;

       struct
       {
           uint8_t vehicleIdx; // Vehicle index of the race winner
       } RaceWinner;

       struct
       {
           uint8_t penaltyType;      // Penalty type – see Appendices
           uint8_t infringementType; // Infringement type – see Appendices
           uint8_t vehicleIdx;       // Vehicle index of the car the penalty is applied to
           uint8_t otherVehicleIdx;  // Vehicle index of the other car involved
           uint8_t time;             // Time gained, or time spent doing action in seconds
           uint8_t lapNum;           // Lap the penalty occurred on
           uint8_t placesGained;     // Number of places gained by this
       } Penalty;

       struct
       {
           uint8_t vehicleIdx; // Vehicle index of the vehicle triggering speed trap
           float speed;        // Top speed achieved in kilometres per hour
       } SpeedTrap;
   };

   struct PacketEventData
   {
       PacketHeader     m_header;               // Header

       uint8_t          m_eventStringCode[4];   // Event string code, see below
       EventDataDetails m_eventDetails;         // Event details - should be interpreted differently
                                                // for each type
   };

""""""""""""""""""
Event String Codes
""""""""""""""""""

+----------------------+--------+------------------------------------------------+
| Event                | Code   | Description                                    |
+======================+========+================================================+
| Session Started      | "SSTA" | Sent when the session starts                   |
+----------------------+--------+------------------------------------------------+
| Session Ended        | "SEND" | Sent when the session ends                     |
+----------------------+--------+------------------------------------------------+
| Fastest Lap          | "FTLP" | When a driver achieves the fastest lap         |
+----------------------+--------+------------------------------------------------+
| Retirement           | "RTMT" | When a driver retires                          |
+----------------------+--------+------------------------------------------------+
| DRS enabled          | "DRSE" | Race control have enabled DRS                  |
+----------------------+--------+------------------------------------------------+
| DRS disabled         | "DRSD" | Race control have disabled DRS                 |
+----------------------+--------+------------------------------------------------+
| Team mate in pits    | "TMPT" | Your team mate has entered the pits            |
+----------------------+--------+------------------------------------------------+
| Chequered flag       | "CHQF" | The chequered flag has been waved              |
+----------------------+--------+------------------------------------------------+
| Race Winner          | "RCWN" | The race winner is announced                   |
+----------------------+--------+------------------------------------------------+
| Penalty Issued       | "PENA" | A penalty has been issued - details in event   |
+----------------------+--------+------------------------------------------------+
| Speed Trap Triggered | "SPTP" | Speed trap has been triggered by fastest speed |
+----------------------+--------+------------------------------------------------+

^^^^^^^^^^^^^^^^^^^
Participants Packet
^^^^^^^^^^^^^^^^^^^

This is a list of participants in the race.
If the vehicle is controlled by AI, then the name will be the driver name.
If this is a multiplayer game, the names will be the Steam Id on PC, or the LAN name if appropriate.

N.B. on Xbox One, the names will always be the driver name, on PS4 the name will be the LAN name if playing a LAN game, otherwise it will be the driver name.

The array should be indexed by vehicle index.

| Frequency: Every 5 seconds
| Size: 1213 bytes
| Version: 1

.. code-block:: c

   struct ParticipantData
   {
       uint8_t    m_aiControlled;           // Whether the vehicle is AI (1) or Human (0) controlled
       uint8_t    m_driverId;               // Driver id - see appendix
       uint8_t    m_teamId;                 // Team id - see appendix
       uint8_t    m_raceNumber;             // Race number of the car
       uint8_t    m_nationality;            // Nationality of the driver
       char       m_name[48];               // Name of participant in UTF-8 format – null terminated
                                            // Will be truncated with … (U+2026) if too long
       uint8_t    m_yourTelemetry;          // The player's UDP setting, 0 = restricted, 1 = public
   };

   struct PacketParticipantsData
   {
       PacketHeader    m_header;            // Header

       uint8           m_numActiveCars;     // Number of active cars in the data – should match number of
                                            // cars on HUD
       ParticipantData m_participants[22];
   };

^^^^^^^^^^^^^^^^^
Car Setups Packet
^^^^^^^^^^^^^^^^^

This packet details the car setups for each vehicle in the session.
Note that in multiplayer games, other player cars will appear as blank, you will only be able to see your car setup and AI cars.

| Frequency: 2 per second
| Size: 1102 bytes
| Version: 1

.. code-block:: c

   struct CarSetupData
   {
       uint8_t   m_frontWing;                // Front wing aero
       uint8_t   m_rearWing;                 // Rear wing aero
       uint8_t   m_onThrottle;               // Differential adjustment on throttle (percentage)
       uint8_t   m_offThrottle;              // Differential adjustment off throttle (percentage)
       float     m_frontCamber;              // Front camber angle (suspension geometry)
       float     m_rearCamber;               // Rear camber angle (suspension geometry)
       float     m_frontToe;                 // Front toe angle (suspension geometry)
       float     m_rearToe;                  // Rear toe angle (suspension geometry)
       uint8_t   m_frontSuspension;          // Front suspension
       uint8_t   m_rearSuspension;           // Rear suspension
       uint8_t   m_frontAntiRollBar;         // Front anti-roll bar
       uint8_t   m_rearAntiRollBar;          // Rear anti-roll bar
       uint8_t   m_frontSuspensionHeight;    // Front ride height
       uint8_t   m_rearSuspensionHeight;     // Rear ride height
       uint8_t   m_brakePressure;            // Brake pressure (percentage)
       uint8_t   m_brakeBias;                // Brake bias (percentage)
       float     m_rearLeftTyrePressure;     // Rear left tyre pressure (PSI)
       float     m_rearRightTyrePressure;    // Rear right tyre pressure (PSI)
       float     m_frontLeftTyrePressure;    // Front left tyre pressure (PSI)
       float     m_frontRightTyrePressure;   // Front right tyre pressure (PSI)
       uint8_t   m_ballast;                  // Ballast
       float     m_fuelLoad;                 // Fuel load
   };

   struct PacketCarSetupData
   {
       PacketHeader    m_header;            // Header

       CarSetupData    m_carSetups[22];
   };

^^^^^^^^^^^^^^^^^^^^
Car Telemetry Packet
^^^^^^^^^^^^^^^^^^^^

This packet details telemetry for all the cars in the race.
It details various values that would be recorded on the car such as speed, throttle application, DRS etc.

| Frequency: Rate as specified in menus
| Size: 1307 bytes
| Version: 1

.. code-block:: c

   struct CarTelemetryData
   {
       uint16_t  m_speed;                      // Speed of car in kilometres per hour
       float     m_throttle;                   // Amount of throttle applied (0.0 to 1.0)
       float     m_steer;                      // Steering (-1.0 (full lock left) to 1.0 (full lock right))
       float     m_brake;                      // Amount of brake applied (0.0 to 1.0)
       uint8_t   m_clutch;                     // Amount of clutch applied (0 to 100)
       int8_t    m_gear;                       // Gear selected (1-8, N=0, R=-1)
       uint16_t  m_engineRPM;                  // Engine RPM
       uint8_t   m_drs;                        // 0 = off, 1 = on
       uint8_t   m_revLightsPercent;           // Rev lights indicator (percentage)
       uint16_t  m_brakesTemperature[4];       // Brakes temperature (celsius)
       uint8_t   m_tyresSurfaceTemperature[4]; // Tyres surface temperature (celsius)
       uint8_t   m_tyresInnerTemperature[4];   // Tyres inner temperature (celsius)
       uint16_t  m_engineTemperature;          // Engine temperature (celsius)
       float     m_tyresPressure[4];           // Tyres pressure (PSI)
       uint8_t   m_surfaceType[4];             // Driving surface, see appendices
   };

   struct PacketCarTelemetryData
   {
       PacketHeader     m_header;             // Header

       CarTelemetryData m_carTelemetryData[22];

       uint32_t         m_buttonStatus;        // Bit flags specifying which buttons are being pressed
                                               // currently - see appendices
       uint8_t          m_mfdPanelIndex;       // Index of MFD panel open - 255 = MFD closed
                                               // Single player, race – 0 = Car setup, 1 = Pits
                                               // 2 = Damage, 3 =  Engine, 4 = Temperatures
                                               // May vary depending on game mode
       uint8_t          m_mfdPanelIndexSecondaryPlayer;   // See above
       int8_t           m_suggestedGear;       // Suggested gear for the player (1-8)
                                               // 0 if no gear suggested
   };

^^^^^^^^^^^^^^^^^
Car Status Packet
^^^^^^^^^^^^^^^^^

This packet details car statuses for all the cars in the race.
It includes values such as the damage readings on the car.

| Frequency: Rate as specified in menus
| Size: 1344 bytes
| Version: 1

.. code-block:: c

   struct CarStatusData
   {
       uint8_t     m_tractionControl;          // 0 (off) - 2 (high)
       uint8_t     m_antiLockBrakes;           // 0 (off) - 1 (on)
       uint8_t     m_fuelMix;                  // Fuel mix - 0 = lean, 1 = standard, 2 = rich, 3 = max
       uint8_t     m_frontBrakeBias;           // Front brake bias (percentage)
       uint8_t     m_pitLimiterStatus;         // Pit limiter status - 0 = off, 1 = on
       float       m_fuelInTank;               // Current fuel mass
       float       m_fuelCapacity;             // Fuel capacity
       float       m_fuelRemainingLaps;        // Fuel remaining in terms of laps (value on MFD)
       uint16_t    m_maxRPM;                   // Cars max RPM, point of rev limiter
       uint16_t    m_idleRPM;                  // Cars idle RPM
       uint8_t     m_maxGears;                 // Maximum number of gears
       uint8_t     m_drsAllowed;               // 0 = not allowed, 1 = allowed, -1 = unknown
       uint16_t    m_drsActivationDistance;    // 0 = DRS not available, non-zero - DRS will be available
                                               // in [X] metres
       uint8_t     m_tyresWear[4];             // Tyre wear percentage
       uint8_t     m_actualTyreCompound;       // F1 Modern - 16 = C5, 17 = C4, 18 = C3, 19 = C2, 20 = C1
                                               // 7 = inter, 8 = wet
                                               // F1 Classic - 9 = dry, 10 = wet
                                               // F2 – 11 = super soft, 12 = soft, 13 = medium, 14 = hard
                                               // 15 = wet
       uint8_t     m_tyreVisualCompound;       // F1 visual (can be different from actual compound)
                                               // 16 = soft, 17 = medium, 18 = hard, 7 = inter, 8 = wet
                                               // F1 Classic – same as above
                                               // F2 – same as above
       uint8_t     m_tyresAgeLaps;             // Age in laps of the current set of tyres
       uint8_t     m_tyresDamage[4];           // Tyre damage (percentage)
       uint8_t     m_frontLeftWingDamage;      // Front left wing damage (percentage)
       uint8_t     m_frontRightWingDamage;     // Front right wing damage (percentage)
       uint8_t     m_rearWingDamage;           // Rear wing damage (percentage)
       uint8_t     m_drsFault;                 // Indicator for DRS fault, 0 = OK, 1 = fault
       uint8_t     m_engineDamage;             // Engine damage (percentage)
       uint8_t     m_gearBoxDamage;            // Gear box damage (percentage)
       int8_t      m_vehicleFiaFlags;          // -1 = invalid/unknown, 0 = none, 1 = green
                                               // 2 = blue, 3 = yellow, 4 = red
       float       m_ersStoreEnergy;           // ERS energy store in Joules
       uint8_t     m_ersDeployMode;            // ERS deployment mode, 0 = none, 1 = medium
                                               // 2 = overtake, 3 = hotlap
       float       m_ersHarvestedThisLapMGUK;  // ERS energy harvested this lap by MGU-K
       float       m_ersHarvestedThisLapMGUH;  // ERS energy harvested this lap by MGU-H
       float       m_ersDeployedThisLap;       // ERS energy deployed this lap
   };

   struct PacketCarStatusData
   {
       PacketHeader     m_header;          // Header

       CarStatusData    m_carStatusData[22];
   };

^^^^^^^^^^^^^^^^^^^^^^^^^^^
Final Classification Packet
^^^^^^^^^^^^^^^^^^^^^^^^^^^

This packet details the final classification at the end of the race, and the data will match with the post race results screen.
This is especially useful for multiplayer games where it is not always possible to send lap times on the final frame because of network delay.

| Frequency: Once at the end of a race
| Size: 839 bytes
| Version: 1

.. code-block:: c

   struct FinalClassificationData
   {
       uint8_t   m_position;              // Finishing position
       uint8_t   m_numLaps;               // Number of laps completed
       uint8_t   m_gridPosition;          // Grid position of the car
       uint8_t   m_points;                // Number of points scored
       uint8_t   m_numPitStops;           // Number of pit stops made
       uint8_t   m_resultStatus;          // Result status - 0 = invalid, 1 = inactive, 2 = active
                                          // 3 = finished, 4 = disqualified, 5 = not classified
                                          // 6 = retired
       float     m_bestLapTime;           // Best lap time of the session in seconds
       double    m_totalRaceTime;         // Total race time in seconds without penalties
       uint8_t   m_penaltiesTime;         // Total penalties accumulated in seconds
       uint8_t   m_numPenalties;          // Number of penalties applied to this driver
       uint8_t   m_numTyreStints;         // Number of tyres stints up to maximum
       uint8_t   m_tyreStintsActual[8];   // Actual tyres used by this driver
       uint8_t   m_tyreStintsVisual[8];   // Visual tyres used by this driver
   };

   struct PacketFinalClassificationData
   {
       PacketHeader               m_header;                  // Header
       uint8                      m_numCars;                 // Number of cars in the final classification
       FinalClassificationData    m_classificationData[22];
   };

^^^^^^^^^^^^^^^^^
Lobby Info Packet
^^^^^^^^^^^^^^^^^

This packet details the players currently in a multiplayer lobby.
It details each player’s selected car, any AI involved in the game and also the ready status of each of the participants.

| Frequency: Two every second when in the lobby
| Size: 1169 bytes
| Version: 1

.. code-block:: c

   struct LobbyInfoData
   {
       uint8_t   m_aiControlled; // Whether the vehicle is AI (1) or Human (0) controlled
       uint8_t   m_teamId;       // Team id - see appendix (255 if no team currently selected)
       uint8_t   m_nationality;  // Nationality of the driver
       char      m_name[48];     // Name of participant in UTF-8 format – null terminated
                                 // Will be truncated with ... (U+2026) if too long
       uint8_t   m_readyStatus;  // 0 = not ready, 1 = ready, 2 = spectating
   };

   struct PacketLobbyInfoData
   {
       PacketHeader        m_header;
       uint8               m_numPlayers; // Number of players in the lobby data
       LobbyInfoData       m_lobbyPlayers[22];
   };

""""""""""""""""""""""""""""""""""""""""
Restricted data (Your Telemetry setting)
""""""""""""""""""""""""""""""""""""""""

There is some data in the UDP that you may not want other players seeing if you are in a multiplayer game.
This is controlled by the “Your Telemetry” setting in the Telemetry options.
The options are:

* Restricted (Default) – other players viewing the UDP data will not see values for your car
* Public – all other players can see all the data for your car

Note: You can always see the data for the car you are driving regardless of the setting.

The following data items are set to zero if the player driving the car in question has their “Your Telemetry” set to “Restricted”:

.. rubric:: Car status packet

* m_fuelInTank
* m_fuelCapacity
* m_fuelMix
* m_fuelRemainingLaps
* m_frontBrakeBias
* m_frontLeftWingDamage
* m_frontRightWingDamage
* m_rearWingDamage
* m_engineDamage
* m_gearBoxDamage
* m_tyresWear (All four wheels)
* m_tyresDamage (All four wheels)
* m_ersDeployMode
* m_ersStoreEnergy
* m_ersDeployedThisLap
* m_ersHarvestedThisLapMGUK
* m_ersHarvestedThisLapMGUH
* m_tyresAgeLaps

----------
Appendices
----------

Here are the values used for the team ID, driver ID and track ID parameters.

N.B. Driver IDs in network games differ from the actual driver IDs.
All the IDs of human players start at 100 and are unique within the game session, but don’t directly correlate to the player.

^^^^^^^^
Team IDs
^^^^^^^^

+----+-----------------+----+-----------------------+----+--------------------------+
| ID | Team            | ID | Team                  | ID | Team                     |
+====+=================+====+=======================+====+==========================+
| 0  | Mercedes        | 21 | Red Bull 2010         | 42 | Art GP '19               |
+----+-----------------+----+-----------------------+----+--------------------------+
| 1  | Ferrari         | 22 | Ferrari 1976          | 43 | Campos '19               |
+----+-----------------+----+-----------------------+----+--------------------------+
| 2  | Red Bull Racing | 23 | ART Grand Prix        | 44 | Carlin '19               |
+----+-----------------+----+-----------------------+----+--------------------------+
| 3  | Williams        | 24 | Campos Vexatec Racing | 45 | Sauber Junior Charouz '19|
+----+-----------------+----+-----------------------+----+--------------------------+
| 4  | Racing Point    | 25 | Carlin                | 46 | Dams '19                 |
+----+-----------------+----+-----------------------+----+--------------------------+
| 5  | Renault         | 26 | Charouz Racing System | 47 | Uni-Virtuosi '19         |
+----+-----------------+----+-----------------------+----+--------------------------+
| 6  | Alpha Tauri     | 27 | DAMS                  | 48 | MP Motorsport '19        |
+----+-----------------+----+-----------------------+----+--------------------------+
| 7  | Haas            | 28 | Russian Time          | 49 | Prema '19                |
+----+-----------------+----+-----------------------+----+--------------------------+
| 8  | McLaren         | 29 | MP Motorsport         | 50 | Trident '19              |
+----+-----------------+----+-----------------------+----+--------------------------+
| 9  | Alfa Romeo      | 30 | Pertamina             | 51 | Arden '19                |
+----+-----------------+----+-----------------------+----+--------------------------+
| 10 | McLaren 1988    | 31 | McLaren 1990          | 53 | Benetton 1994            |
+----+-----------------+----+-----------------------+----+--------------------------+
| 11 | McLaren 1991    | 32 | Trident               | 54 | Benetton 1995            |
+----+-----------------+----+-----------------------+----+--------------------------+
| 12 | Williams 1992   | 33 | BWT Arden             | 55 | Ferrari 2000             |
+----+-----------------+----+-----------------------+----+--------------------------+
| 13 | Ferrari 1995    | 34 | McLaren 1976          | 56 | Jordan 1991              |
+----+-----------------+----+-----------------------+----+--------------------------+
| 14 | Williams 1996   | 35 | Lotus 1972            |    |                          |
+----+-----------------+----+-----------------------+----+--------------------------+
| 15 | McLaren 1998    | 36 | Ferrari 1979          |    |                          |
+----+-----------------+----+-----------------------+----+--------------------------+
| 16 | Ferrari 2002    | 37 | McLaren 1982          |    |                          |
+----+-----------------+----+-----------------------+----+--------------------------+
| 17 | Ferrari 2004    | 38 | Williams 2003         |    |                          |
+----+-----------------+----+-----------------------+----+--------------------------+
| 18 | Renault 2006    | 39 | Brawn 2009            |    |                          |
+----+-----------------+----+-----------------------+----+--------------------------+
| 19 | Ferrari 2007    | 40 | Lotus 1978            |    |                          |
+----+-----------------+----+-----------------------+----+--------------------------+
| 20 | McLaren 2008    | 41 | F1 Generic car        | 255| My Team                  |
+----+-----------------+----+-----------------------+----+--------------------------+

^^^^^^^^^^
Driver IDs
^^^^^^^^^^

+----+--------------------+----+---------------------+----+----------------------+
| ID | Driver             | ID | Driver              | ID | Driver               |
+====+====================+====+=====================+====+======================+
| 0  | Carlos Sainz       | 37 | Peter Belousov      | 70 | Rashid Nair          |
+----+--------------------+----+---------------------+----+----------------------+
| 1  | Daniil Kvyat       | 38 | Klimek Michalski    | 71 | Jack Tremblay        |
+----+--------------------+----+---------------------+----+----------------------+
| 2  | Daniel Ricciardo   | 39 | Santiago Moreno     | 74 | Antonio Giovinazzi   |
+----+--------------------+----+---------------------+----+----------------------+
| 6  | Kimi Räikkönen     | 40 | Benjamin Coppens    | 75 | Robert Kubica        |
+----+--------------------+----+---------------------+----+----------------------+
| 7  | Lewis Hamilton     | 41 | Noah Visser         | 78 | Robuharu Matsushita  |
+----+--------------------+----+---------------------+----+----------------------+
| 9  | Max Verstappen     | 42 | Gert Waldmuller     | 79 | Nikita Mazepin       |
+----+--------------------+----+---------------------+----+----------------------+
| 10 | Nico Hulkenberg    | 43 | Julian Quesada      | 80 | Guanya Zhou          |
+----+--------------------+----+---------------------+----+----------------------+
| 11 | Kevin Magnussen    | 44 | Daniel Jones        | 81 | Mick Schumacher      |
+----+--------------------+----+---------------------+----+----------------------+
| 12 | Romain Grosjean    | 45 | Artem Markelov      | 82 | Callum Ilott         |
+----+--------------------+----+---------------------+----+----------------------+
| 13 | Sebastian Vettel   | 46 | Tadasuke Makino     | 83 | Juan Manuel Correa   |
+----+--------------------+----+---------------------+----+----------------------+
| 14 | Sergio Perez       | 47 | Sean Gelael         | 84 | Jordan King          |
+----+--------------------+----+---------------------+----+----------------------+
| 15 | Valtteri Bottas    | 48 | Nyck De Vries       | 85 | Mahaveer Raghunathan |
+----+--------------------+----+---------------------+----+----------------------+
| 17 | Esteban Ocon       | 49 | Jack Aitken         | 86 | Tatiana Calderon     |
+----+--------------------+----+---------------------+----+----------------------+
| 19 | Lance Stroll       | 50 | George Russell      | 87 | Anthoine Hubert      |
+----+--------------------+----+---------------------+----+----------------------+
| 20 | Arron Barnes       | 51 | Maximilian Günther  | 88 | Guiliano Alesi       |
+----+--------------------+----+---------------------+----+----------------------+
| 21 | Martin Giles       | 52 | Nirei Fukuzumi      | 89 | Ralph Boschung       |
+----+--------------------+----+---------------------+----+----------------------+
| 22 | Alex Murray        | 53 | Luca Ghiotto        |    |                      |
+----+--------------------+----+---------------------+----+----------------------+
| 23 | Lucas Roth         | 54 | Lando Norris        |    |                      |
+----+--------------------+----+---------------------+----+----------------------+
| 24 | Igor Correia       | 55 | Sérgio Sette Câmara |    |                      |
+----+--------------------+----+---------------------+----+----------------------+
| 25 | Sophie Levasseur   | 56 | Louis Delétraz      |    |                      |
+----+--------------------+----+---------------------+----+----------------------+
| 26 | Jonas Schiffer     | 57 | Antonio Fuoco       |    |                      |
+----+--------------------+----+---------------------+----+----------------------+
| 27 | Alain Forest       | 58 | Charles Leclerc     |    |                      |
+----+--------------------+----+---------------------+----+----------------------+
| 28 | Jay Letourneau     | 59 | Pierre Gasly        |    |                      |
+----+--------------------+----+---------------------+----+----------------------+
| 29 | Esto Saari         | 62 | Alexander Albon     |    |                      |
+----+--------------------+----+---------------------+----+----------------------+
| 30 | Yasar Atiyeh       | 63 | Nicholas Latifi     |    |                      |
+----+--------------------+----+---------------------+----+----------------------+
| 31 | Callisto Calabresi | 64 | Dorian Boccolacci   |    |                      |
+----+--------------------+----+---------------------+----+----------------------+
| 32 | Naota Izum         | 65 | Niko Kari           |    |                      |
+----+--------------------+----+---------------------+----+----------------------+
| 33 | Howard Clarke      | 66 | Roberto Merhi       |    |                      |
+----+--------------------+----+---------------------+----+----------------------+
| 34 | Wilhelm Kaufmann   | 67 | Arjun Maini         |    |                      |
+----+--------------------+----+---------------------+----+----------------------+
| 35 | Marie Laursen      | 68 | Alessio Lorandi     |    |                      |
+----+--------------------+----+---------------------+----+----------------------+
| 36 | Flavio Nieves      | 69 | Ruben Meijer        |    |                      |
+----+--------------------+----+---------------------+----+----------------------+

^^^^^^^^^
Track IDs
^^^^^^^^^

+----+-------------------+
| ID | Track             |
+====+===================+
| 0  | Melbourne         |
+----+-------------------+
| 1  | Paul Ricard       |
+----+-------------------+
| 2  | Shanghai          |
+----+-------------------+
| 3  | Sakhir (Bahrain)  |
+----+-------------------+
| 4  | Catalunya         |
+----+-------------------+
| 5  | Monaco            |
+----+-------------------+
| 6  | Montreal          |
+----+-------------------+
| 7  | Silverstone       |
+----+-------------------+
| 8  | Hockenheim        |
+----+-------------------+
| 9  | Hungaroring       |
+----+-------------------+
| 10 | Spa               |
+----+-------------------+
| 11 | Monza             |
+----+-------------------+
| 12 | Singapore         |
+----+-------------------+
| 13 | Suzuka            |
+----+-------------------+
| 14 | Abu Dhabi         |
+----+-------------------+
| 15 | Texas             |
+----+-------------------+
| 16 | Brazil            |
+----+-------------------+
| 17 | Austria           |
+----+-------------------+
| 18 | Sochi             |
+----+-------------------+
| 19 | Mexico            |
+----+-------------------+
| 20 | Baku (Azerbaijan) |
+----+-------------------+
| 21 | Sakhir Short      |
+----+-------------------+
| 22 | Silverstone Short |
+----+-------------------+
| 23 | Texas Short       |
+----+-------------------+
| 24 | Suzuka Short      |
+----+-------------------+
| 25 | Hanoi             |
+----+-------------------+
| 26 | Zandvoort         |
+----+-------------------+

^^^^^^^^^^^^^^^
Nationality IDs
^^^^^^^^^^^^^^^

+----+-------------+----+----------------+----+---------------+
| ID | Nationality | ID | Nationality    | ID | Nationality   |
+====+=============+====+================+====+===============+
| 1  | American    | 31 | Greek          | 61 | Panamanian    |
+----+-------------+----+----------------+----+---------------+
| 2  | Argentinian | 32 | Guatemalan     | 62 | Paraguayan    |
+----+-------------+----+----------------+----+---------------+
| 3  | Australian  | 33 | Honduran       | 63 | Peruvian      |
+----+-------------+----+----------------+----+---------------+
| 4  | Austrian    | 34 | Hong Konger    | 64 | Polish        |
+----+-------------+----+----------------+----+---------------+
| 5  | Azerbaijani | 35 | Hungarian      | 65 | Portuguese    |
+----+-------------+----+----------------+----+---------------+
| 6  | Bahraini    | 36 | Icelander      | 66 | Qatari        |
+----+-------------+----+----------------+----+---------------+
| 7  | Belgian     | 37 | Indian         | 67 | Romanian      |
+----+-------------+----+----------------+----+---------------+
| 8  | Bolivian    | 38 | Indonesian     | 68 | Russian       |
+----+-------------+----+----------------+----+---------------+
| 9  | Brazilian   | 39 | Irish          | 69 | Salvadoran    |
+----+-------------+----+----------------+----+---------------+
| 10 | British     | 40 | Israeli        | 70 | Saudi         |
+----+-------------+----+----------------+----+---------------+
| 11 | Bulgarian   | 41 | Italian        | 71 | Scottish      |
+----+-------------+----+----------------+----+---------------+
| 12 | Cameroonian | 42 | Jamaican       | 72 | Serbian       |
+----+-------------+----+----------------+----+---------------+
| 13 | Canadian    | 43 | Japanese       | 73 | Singaporean   |
+----+-------------+----+----------------+----+---------------+
| 14 | Chilean     | 44 | Jordanian      | 74 | Slovakian     |
+----+-------------+----+----------------+----+---------------+
| 15 | Chinese     | 45 | Kuwaiti        | 75 | Slovenian     |
+----+-------------+----+----------------+----+---------------+
| 16 | Colombian   | 46 | Latvian        | 76 | South Korean  |
+----+-------------+----+----------------+----+---------------+
| 17 | Costa Rican | 47 | Lebanese       | 77 | South African |
+----+-------------+----+----------------+----+---------------+
| 18 | Croatian    | 48 | Lithuanian     | 78 | Spanish       |
+----+-------------+----+----------------+----+---------------+
| 19 | Cypriot     | 49 | Luxembourger   | 79 | Swedish       |
+----+-------------+----+----------------+----+---------------+
| 20 | Czech       | 50 | Malaysian      | 80 | Swiss         |
+----+-------------+----+----------------+----+---------------+
| 21 | Danish      | 51 | Maltese        | 81 | Thai          |
+----+-------------+----+----------------+----+---------------+
| 22 | Dutch       | 52 | Mexican        | 82 | Turkish       |
+----+-------------+----+----------------+----+---------------+
| 23 | Ecuadorian  | 53 | Monegasque     | 83 | Uruguayan     |
+----+-------------+----+----------------+----+---------------+
| 24 | English     | 54 | New Zealander  | 84 | Ukrainian     |
+----+-------------+----+----------------+----+---------------+
| 25 | Emirian     | 55 | Nicaraguan     | 85 | Venezuelan    |
+----+-------------+----+----------------+----+---------------+
| 26 | Estonian    | 56 | North Korean   | 86 | Welsh         |
+----+-------------+----+----------------+----+---------------+
| 27 | Finnish     | 57 | Northern Irish | 87 | Barbadian     |
+----+-------------+----+----------------+----+---------------+
| 28 | French      | 58 | Norwegian      | 88 | Vietnamese    |
+----+-------------+----+----------------+----+---------------+
| 29 | German      | 59 | Omani          |    |               |
+----+-------------+----+----------------+----+---------------+
| 30 | Ghanaian    | 60 | Pakistani      |    |               |
+----+-------------+----+----------------+----+---------------+

^^^^^^^^^^^^^
Surface types
^^^^^^^^^^^^^

These types are from physics data and show what type of contact each wheel is experiencing.

+----+--------------+
| ID | Surface      |
+====+==============+
| 0  | Tarmac       |
+----+--------------+
| 1  | Rumble strip |
+----+--------------+
| 2  | Concrete     |
+----+--------------+
| 3  | Rock         |
+----+--------------+
| 4  | Gravel       |
+----+--------------+
| 5  | Mud          |
+----+--------------+
| 6  | Sand         |
+----+--------------+
| 7  | Grass        |
+----+--------------+
| 8  | Water        |
+----+--------------+
| 9  | Cobblestone  |
+----+--------------+
| 10 | Metal        |
+----+--------------+
| 11 | Ridged       |
+----+--------------+

^^^^^^^^^^^^
Button flags
^^^^^^^^^^^^

These flags are used in the telemetry packet to determine if any buttons are being held on the controlling device. If the value below logical ANDed with the button status is set then the corresponding button is being held.

+-----------+-------------------+
| Bit flags | Button            |
+===========+===================+
| 0x0001    | Cross or A        |
+-----------+-------------------+
| 0x0002    | Triangle or Y     |
+-----------+-------------------+
| 0x0004    | Circle or B       |
+-----------+-------------------+
| 0x0008    | Square or X       |
+-----------+-------------------+
| 0x0010    | D-pad Left        |
+-----------+-------------------+
| 0x0020    | D-pad Right       |
+-----------+-------------------+
| 0x0040    | D-pad Up          |
+-----------+-------------------+
| 0x0080    | D-pad Down        |
+-----------+-------------------+
| 0x0100    | Options or Menu   |
+-----------+-------------------+
| 0x0200    | L1 or LB          |
+-----------+-------------------+
| 0x0400    | R1 or RB          |
+-----------+-------------------+
| 0x0800    | L2 or LT          |
+-----------+-------------------+
| 0x1000    | R2 or RT          |
+-----------+-------------------+
| 0x2000    | Left Stick Click  |
+-----------+-------------------+
| 0x4000    | Right Stick Click |
+-----------+-------------------+

^^^^^^^^^^^^^
Penalty types
^^^^^^^^^^^^^

+----+--------------------------------------------------+
| ID | Penalty meaning                                  |
+====+==================================================+
| 0  | Drive through                                    |
+----+--------------------------------------------------+
| 1  | Stop Go                                          |
+----+--------------------------------------------------+
| 2  | Grid penalty                                     |
+----+--------------------------------------------------+
| 3  | Penalty reminder                                 |
+----+--------------------------------------------------+
| 4  | Time penalty                                     |
+----+--------------------------------------------------+
| 5  | Warning                                          |
+----+--------------------------------------------------+
| 6  | Disqualified                                     |
+----+--------------------------------------------------+
| 7  | Removed from formation lap                       |
+----+--------------------------------------------------+
| 8  | Parked too long timer                            |
+----+--------------------------------------------------+
| 9  | Tyre regulations                                 |
+----+--------------------------------------------------+
| 10 | This lap invalidated                             |
+----+--------------------------------------------------+
| 11 | This and next lap invalidated                    |
+----+--------------------------------------------------+
| 12 | This lap invalidated without reason              |
+----+--------------------------------------------------+
| 13 | This and next lap invalidated without reason     |
+----+--------------------------------------------------+
| 14 | This and previous lap invalidated                |
+----+--------------------------------------------------+
| 15 | This and previous lap invalidated without reason |
+----+--------------------------------------------------+
| 16 | Retired                                          |
+----+--------------------------------------------------+
| 17 | Black flag timer                                 |
+----+--------------------------------------------------+

^^^^^^^^^^^^^^^^^^
Infringement types
^^^^^^^^^^^^^^^^^^

+----+--------------------------------------------------+
| ID | Infringement meaning                             |
+====+==================================================+
| 0  | Blocking by slow driving                         |
+----+--------------------------------------------------+
| 1  | Blocking by wrong way driving                    |
+----+--------------------------------------------------+
| 2  | Reversing off the start line                     |
+----+--------------------------------------------------+
| 3  | Big Collision                                    |
+----+--------------------------------------------------+
| 4  | Small Collision                                  |
+----+--------------------------------------------------+
| 5  | Collision failed to hand back position single    |
+----+--------------------------------------------------+
| 6  | Collision failed to hand back position multiple  |
+----+--------------------------------------------------+
| 7  | Corner cutting gained time                       |
+----+--------------------------------------------------+
| 8  | Corner cutting overtake single                   |
+----+--------------------------------------------------+
| 9  | Corner cutting overtake multiple                 |
+----+--------------------------------------------------+
| 10 | Crossed pit exit lane                            |
+----+--------------------------------------------------+
| 11 | Ignoring blue flags                              |
+----+--------------------------------------------------+
| 12 | Ignoring yellow flags                            |
+----+--------------------------------------------------+
| 13 | Ignoring drive through                           |
+----+--------------------------------------------------+
| 14 | Too many drive throughs                          |
+----+--------------------------------------------------+
| 15 | Drive through reminder serve within n laps       |
+----+--------------------------------------------------+
| 16 | Drive through reminder serve this lap            |
+----+--------------------------------------------------+
| 17 | Pit lane speeding                                |
+----+--------------------------------------------------+
| 18 | Parked for too long                              |
+----+--------------------------------------------------+
| 19 | Ignoring tyre regulations                        |
+----+--------------------------------------------------+
| 20 | Too many penalties                               |
+----+--------------------------------------------------+
| 21 | Multiple warnings                                |
+----+--------------------------------------------------+
| 22 | Approaching disqualification                     |
+----+--------------------------------------------------+
| 23 | Tyre regulations select single                   |
+----+--------------------------------------------------+
| 24 | Tyre regulations select multiple                 |
+----+--------------------------------------------------+
| 25 | Lap invalidated corner cutting                   |
+----+--------------------------------------------------+
| 26 | Lap invalidated running wide                     |
+----+--------------------------------------------------+
| 27 | Corner cutting ran wide gained time minor        |
+----+--------------------------------------------------+
| 28 | Corner cutting ran wide gained time significant  |
+----+--------------------------------------------------+
| 29 | Corner cutting ran wide gained time extreme      |
+----+--------------------------------------------------+
| 30 | Lap invalidated wall riding                      |
+----+--------------------------------------------------+
| 31 | Lap invalidated flashback used                   |
+----+--------------------------------------------------+
| 32 | Lap invalidated reset to track                   |
+----+--------------------------------------------------+
| 33 | Blocking the pitlane                             |
+----+--------------------------------------------------+
| 34 | Jump start                                       |
+----+--------------------------------------------------+
| 35 | Safety car to car collision                      |
+----+--------------------------------------------------+
| 36 | Safety car illegal overtake                      |
+----+--------------------------------------------------+
| 37 | Safety car exceeding allowed pace                |
+----+--------------------------------------------------+
| 38 | Virtual safety car exceeding allowed pace        |
+----+--------------------------------------------------+
| 39 | Formation lap below allowed speed                |
+----+--------------------------------------------------+
| 40 | Retired mechanical failure                       |
+----+--------------------------------------------------+
| 41 | Retired terminally damaged                       |
+----+--------------------------------------------------+
| 42 | Safety car falling too far back                  |
+----+--------------------------------------------------+
| 43 | Black flag timer                                 |
+----+--------------------------------------------------+
| 44 | Unserved stop go penalty                         |
+----+--------------------------------------------------+
| 45 | Unserved drive through penalty                   |
+----+--------------------------------------------------+
| 46 | Engine component change                          |
+----+--------------------------------------------------+
| 47 | Gearbox change                                   |
+----+--------------------------------------------------+
| 48 | League grid penalty                              |
+----+--------------------------------------------------+
| 49 | Retry penalty                                    |
+----+--------------------------------------------------+
| 50 | Illegal time gain                                |
+----+--------------------------------------------------+
| 51 | Mandatory pitstop                                |
+----+--------------------------------------------------+
